"""
This is the application entrypoint.

It supports two modes (Assuming you are are in the 'src/dora' directory):
1.  File Mode: Runs the analysis based on a specified YAML config file.
    (e.g., `python main.py --config config.yaml`)
2.  Interactive Mode: If no config file is given, it launches a setup wizard.
    (e.g., `python main.py`)
"""

import cProfile
import io
import logging
import pstats
from importlib import metadata
from pathlib import Path

import pandas as pd
import typer
import yaml
from rich import print as rprint

from dora.analyzer import Analyzer
from dora.config_loader import load_config
from dora.data_loader import read_data
from dora.kaggle import KaggleHandler
from dora.schema import (AnalysisStep, BivariateStep, Config, MultivariateStep,
                         ProfileStep, UnivariateStep)

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

app = typer.Typer(help="DORA: The Data-Oriented Report Automator")


def version_callback(value: bool) -> None:
    """
    Callback function to display the version and exit.

    :param value: Whether to display the version or not.
    :return: None
    """
    if value:
        # We fetch the version directly from the installed package metadata.
        # Since 'dora-eda' is defined in pyproject.toml, this will retrieve
        # that exact version string as long as the package is installed.
        version = metadata.version("dora-eda")
        rprint(f"DORA v{version}")
        raise typer.Exit()


def handle_kaggle_download(dataset_id: str) -> Path:
    """
    Wrapper to handle the kaggle download

    :param dataset_id: Kaggle dataset ID e.g. 'owner/dataset-name'
    :returns: Path to downloaded dataset file
    """
    rprint(f"[cyan]Downloading dataset {dataset_id}...[/cyan]")

    try:
        file_path = KaggleHandler.download_dataset(dataset_id)
        rprint(f"[green]Download complete. Using file {file_path.name}[/green]")
        return file_path
    except ValueError as e:
        rprint(f"[bold red]{e}[/bold red]")
        raise typer.Exit(code=1) from e
    except RuntimeError as e:
        rprint(f"[bold red]{e}[/bold red]")
        raise typer.Exit(code=1) from e
    except Exception as e:
        rprint(
            f"[bold red]An unexpected error occurred during download: {e}[/bold red]"
        )
        raise typer.Exit(code=1) from e


def create_config_interactively() -> tuple[pd.DataFrame, Config]:
    """
    Guides the user through an interactive CLI session to build the config.

    :returns: Tuple containing pandas dataframe and configuration file
    """
    rprint("[bold blue]DORA Interactive Setup Wizard[/bold blue]")
    rprint("Let's configure your EDA report step by step.")

    # We loop until a valid file is provided to prevent the program from crashing later on.
    while True:
        input_str = typer.prompt(
            "📁 Enter local file path OR Kaggle URL/ID (Example: 'owner/dataset-name')"
        )
        if KaggleHandler.is_kaggle_url(input_str):
            dataset_id = KaggleHandler.extract_dataset_id(input_str)
            if typer.confirm(f"Download Kaggle dataset '{dataset_id}'?", default=True):
                input_file = handle_kaggle_download(dataset_id)
            else:
                continue
        else:
            input_file = Path(input_str)

        if input_file.exists() and input_file.is_file():
            try:
                df = read_data(input_file)
                # If the file is read successfully, we can exit the loop.
                break
            except Exception as e:
                rprint(f"[bold red]Error reading file: {e}[/bold red]")
        else:
            rprint("[bold red]File not found. Please enter a valid path.[/bold red]")

    # Personalizing the output makes the final report feel more professional and easier to identify later.
    output_dir = typer.prompt("📂 Enter the output directory", default="output")
    default_title = f"EDA Report for {input_file.stem}"
    report_title = typer.prompt("📝 Enter the report title", default=default_title)

    assert type(df) is pd.DataFrame
    # Knowing the target variable allows DORA to create more focused and insightful plots (like feature vs. target),
    # which is often the main goal of EDA.
    rprint("\n[bold]Available columns:[/bold]")
    rprint(df.columns.tolist())
    target_variable = typer.prompt(
        "🎯 Enter the target variable (or press Enter to skip)",
        default="",
        show_default=False,
    )
    # We validate the user's input to ensure it's a real column, which prevents errors during the analysis phase.
    if not target_variable or target_variable not in df.columns:
        if target_variable:
            rprint(
                f"[yellow]Warning: Column '{target_variable}' not found. Proceeding without a target.[/yellow]"
            )
        target_variable = None

    # This is where we gather all the user's choices into a single, structured "plan" that the Analyzer will execute.
    pipeline = []

    # To give the user full control, we ask them to opt-in to each analysis step.
    # This makes the tool flexible for both quick overviews and deep dives.
    rprint("\n[bold blue]Select the analysis steps to perform:[/bold blue]")
    if typer.confirm(
        "📊 Generate Data Profile (overview, missing values, etc.)?", default=True
    ):
        pipeline.append(AnalysisStep(profile=ProfileStep(enabled=True)))

    if typer.confirm(
        "📈 Generate Univariate Analysis (plots for single columns)?", default=True
    ):
        pipeline.append(
            AnalysisStep(
                univariate=UnivariateStep(
                    enabled=True,
                    plot_types={
                        "numerical": ["histogram", "boxplot"],
                        "categorical": ["barplot"],
                    },
                )
            )
        )

    if target_variable and typer.confirm(
        f"🔗 Generate Bivariate Analysis (features vs. '{target_variable}')?",
        default=True,
    ):
        pipeline.append(
            AnalysisStep(bivariate=BivariateStep(enabled=True, target_centric=True))
        )

    if typer.confirm(
        "🌐 Generate Multivariate Analysis (correlation matrix)?", default=True
    ):
        pipeline.append(
            AnalysisStep(
                multivariate=MultivariateStep(enabled=True, correlation_cols=[])
            )
        )

    config = Config(
        input_file=input_file,
        output_dir=Path(output_dir),
        report_title=report_title,
        target_variable=target_variable,
        analysis_pipeline=pipeline,
    )

    return df, config


@app.command()
def run(
    config_path: Path = typer.Option(
        # Default to None to trigger interactive mode
        None,
        "--config",
        "-c",
        help="Path to a configuration YAML file. If not provided, starts interactive mode.",
        file_okay=True,
        dir_okay=False,
        readable=True,
    ),
    profile: bool = typer.Option(
        False,
        "--profile",
        is_flag=True,
        help="Enable performance profiling and print the results.",
    ),
    version: bool = typer.Option(
        None,
        "--version",
        "-v",
        callback=version_callback,
        is_eager=True,
        help="Show the application version and exit.",
    ),
):
    """
    Runs the automated EDA process either from a config file or via an interactive wizard.
    """
    profiler = None
    if profile:
        # If profiling is enabled, wrap the main execution in the profiler.
        profiler = cProfile.Profile()
        profiler.enable()

    config = None
    df = None

    # This top-level try/except is a safety net. It ensures that if anything unexpected goes wrong,
    # the user gets a clean error message instead of a scary wall of red text lol.
    try:
        if config_path:
            # File Mode
            # This is the "fast lane" for repeat users. If a config file is provided,
            # we can skip the interactive setup and get straight to the analysis.
            logging.info("Running in File Mode.")
            if not config_path.exists():
                rprint(
                    "[bold red]Error: Config file not found at %s [/bold red]",
                    config_path,
                )
                raise typer.Exit(code=1)

            logging.info("Loading configuration from: %s", config_path)
            config = load_config(config_path)

            if not config.input_file.exists():
                raise FileNotFoundError(f"Input file not found: {config.input_file}")

            logging.info("Loading data from: %s", config.input_file)
            df = read_data(config.input_file)
        else:
            # Interactive Mode
            # If no config file is passed, we enter the guided setup. This makes
            # the tool user-friendly for first-time use or new datasets.
            df, config = create_config_interactively()

            # To save the user time on future runs, we offer to save their choices into a reusable config file.
            if typer.confirm(
                "\n💾 Save this configuration to 'config.yaml' for future use?"
            ):
                with open("config.yaml", "w", encoding="utf-8") as f:
                    yaml.dump(config.model_dump(mode="json"), f, sort_keys=False)
                rprint("[green]Configuration saved to 'config.yaml'.[/green]")

        # Run Analysis
        # Once the configuration is ready (either from a file or the wizard),
        # we hand it over to the Analyzer to do the heavy lifting.
        logging.info("Initializing EDA Analyzer...")
        analyzer = Analyzer(df, config)

        logging.info("Starting analysis pipeline...")
        analyzer.run()

        logging.info("✅ Analysis complete! Report saved in: %s", config.output_dir)

    except FileNotFoundError as e:
        logging.error("Error: Input file not found. %s", e)
        raise typer.Exit(code=1)
    except Exception as e:
        logging.error("An unexpected error occurred: %s", e, exc_info=True)
        raise typer.Exit(code=1)
    finally:
        # This block ensures that the profiler results are printed even if an error occurs.
        if profiler:
            profiler.disable()
            rprint("\n[bold magenta] --- Performance Profile --- [/bold magenta]")
            s = io.StringIO()
            # Sort by cumulative time spent in functions
            ps = pstats.Stats(profiler, stream=s).sort_stats("cumulative")
            ps.print_stats(30)
            rprint(s.getvalue())

            # Save full stats to a file for more detailed analysis
            profile_output_file = "dora_profile.prof"
            profiler.dump_stats(profile_output_file)
            rprint(
                f"[green]Full profiling stats saved to '{profile_output_file}'.[/green]"
            )
            rprint(
                "Tip: Use a tool like 'snakeviz' to visualize the results (`pip install snakeviz` then `snakeviz dora_profile.prof`)"
            )


def main():
    app()


if __name__ == "__main__":
    app()
