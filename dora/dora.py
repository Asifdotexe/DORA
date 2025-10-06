import argparse
import pandas as pd
import os
import logging
from tqdm import tqdm
from dataclasses import dataclass
from src.univariate_analysis import univariate_analysis
from src.bivariate_analysis import bivariate_analysis
from src.multivariate_analysis import multivariate_analysis
from src.save_results import save_results

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

@dataclass
class DORA:
    """Class for performing Exploratory Data Analysis (EDA) and creating a PowerPoint presentation.

    :param input_file: Path to the input CSV file.
    :param output_dir: Directory where output will be saved.
    :param template_path: Optional path to PowerPoint template.
    """
    input_file: str
    output_dir: str
    template_path: str = None

    def print_separator(self):
        """Print a separator line for better visibility in console output."""
        print("\n" + "=" * 80 + "\n")

    def process(self):
        """Load data, perform EDA, and save results in PowerPoint format."""
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(f"{self.output_dir}/stats/", exist_ok=True)
        os.makedirs(f"{self.output_dir}/charts/", exist_ok=True)

        self.print_separator()
        logging.info("\033[34mLoading data...\033[0m")
        df = pd.read_csv(self.input_file)

        tasks = [
            ("\033[93mUnivariate Analysis\033[0m", univariate_analysis),  # Yellow-colored task
            ("\033[93mBivariate Analysis\033[0m", bivariate_analysis),    # Yellow-colored task
            ("\033[93mMultivariate Analysis\033[0m", multivariate_analysis) # Yellow-colored task
        ]

        self.print_separator()
        logging.info("\033[34mStarting Exploratory Data Analysis (EDA)...\033[0m")

        # Iterate over the list of tasks to perform each type of analysis.
        for task_name, analysis_func in tqdm(
            tasks,
            desc="Performing EDA",
            ncols=100,
            unit="task",
            bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} {elapsed_s:.2f}s",
            ascii=" |.|",
        ):
            self.print_separator()
            logging.info(f"Starting {task_name}...")
            # Call the respective analysis function with the DataFrame and output directory.
            analysis_func(df, self.output_dir)
            logging.info(f"Completed {task_name}.")

        self.print_separator()
        logging.info("\033[93mSaving results and creating PowerPoint presentation...\033[0m")
        # Save the results and create a PowerPoint presentation.
        save_results(self.output_dir, self.template_path)
        logging.info(f"\033[93mPresentation created successfully.\033[0m")
        self.print_separator()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Perform EDA and create a PowerPoint presentation.")
    parser.add_argument("input_file", type=str, help="Path to the input CSV file.")
    parser.add_argument("output_dir", type=str, help="Directory where output will be saved.")
    parser.add_argument("--template_path", type=str, default=None, help="Optional path to PowerPoint template.")
    args = parser.parse_args()

    eda_processor = DORA(args.input_file, args.output_dir, args.template_path)
    eda_processor.process()
