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

logger = logging.getLogger(__name__)
import pstats
from importlib import metadata
from pathlib import Path

import pandas as pd
import typer
import yaml
from rich import print as rprint

from dora.analyzer import run_analysis
from dora.config_loader import load_config
from dora.data_loader import read_data
from dora.kaggle import download_dataset, extract_dataset_id, is_kaggle_url
from dora.schema import Config

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

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
        file_path = download_dataset(dataset_id)
        rprint(f"[green]Download complete. Using file {file_path.name}[/green]")
        return file_path
    except ValueError as e:
        rprint(f"[bold red]{e}[/bold red]")
        raise typer.Exit(code=1) from e
    except RuntimeError as e:
        rprint(f"[bold red]{e}[/bold red]")
        raise typer.Exit(code=1) from e
    except OSError as e:
        rprint(f"[bold red]An unexpected error occurred during download: {e}[/bold red]")
        raise typer.Exit(code=1) from e


def create_config_interactively() -> tuple[pd.DataFrame, Config]:
    """
    Launches the full-screen TUI to build the config, then processes it.
    """
    from dora.tui import DoraTUI

    app = DoraTUI()
    result = app.run(inline=True)

    if not result:
        rprint("\n[bold cyan]Thanks for using DORA! Goodbye.[/bold cyan]")
        raise typer.Exit()

    input_str = result["input_file"]

    if is_kaggle_url(input_str):
        dataset_id = extract_dataset_id(input_str)
        input_file = handle_kaggle_download(dataset_id)
    else:
        input_file = Path(input_str)

    if not input_file.exists() or not input_file.is_file():
        rprint("[bold red]File not found. Please provide a valid path.[/bold red]")
        raise typer.Exit(code=1)

    try:
        df = read_data(input_file)
    except (ValueError, OSError, RuntimeError) as e:
        rprint(f"[bold red]Error reading file: {e}[/bold red]")
        raise typer.Exit(code=1)

    assert type(df) is pd.DataFrame
    target_variable = result["target_variable"]
    if target_variable and target_variable not in df.columns:
        rprint(f"[yellow]Warning: Column '{target_variable}' not found. Proceeding without a target.[/yellow]")
        target_variable = None

    config = Config(
        input_file=input_file,
        output_dir=Path(result["output_dir"]),
        report_title=result["report_title"],
        target_variable=target_variable,
        profile_enabled=result["profile_enabled"],
        univariate_enabled=result["univariate_enabled"],
        bivariate_enabled=result["bivariate_enabled"],
        multivariate_enabled=result["multivariate_enabled"],
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
            logger.info("Running in File Mode.")
            if not config_path.exists():
                rprint(
                    "[bold red]Error: Config file not found at %s [/bold red]",
                    config_path,
                )
                raise typer.Exit(code=1)

            logger.info("Loading configuration from: %s", config_path)
            config = load_config(config_path)

            if not config.input_file.exists():
                raise FileNotFoundError(f"Input file not found: {config.input_file}")

            logger.info("Loading data from: %s", config.input_file)
            df = read_data(config.input_file)
        else:
            # Interactive Mode
            # If no config file is passed, we enter the guided setup. This makes
            # the tool user-friendly for first-time use or new datasets.
            df, config = create_config_interactively()

            # To save the user time on future runs, we offer to save their choices into a reusable config file.
            if typer.confirm("\n💾 Save this configuration to 'config.yaml' for future use?"):
                with open("config.yaml", "w", encoding="utf-8") as f:
                    yaml.dump(config.model_dump(mode="json"), f, sort_keys=False)
                rprint("[green]Configuration saved to 'config.yaml'.[/green]")

        # Run Analysis
        # Once the configuration is ready (either from a file or the wizard),
        # we hand it over to the Analyzer to do the heavy lifting.
        logger.info("Starting analysis pipeline...")
        run_analysis(df, config)

        logger.info("✅ Analysis complete! Report saved in: %s", config.output_dir)

    except typer.Exit:
        raise
    except FileNotFoundError as e:
        logger.error("Error: Input file not found. %s", e)
        raise typer.Exit(code=1)
    except (ValueError, OSError, RuntimeError):
        logger.exception("An unexpected error occurred")
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
            rprint(f"[green]Full profiling stats saved to '{profile_output_file}'.[/green]")
            rprint(
                "Tip: Use a tool like 'snakeviz' to visualize the results (`pip install snakeviz` then `snakeviz dora_profile.prof`)"
            )


def main():
    app()


if __name__ == "__main__":
    app()
