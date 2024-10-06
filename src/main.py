import argparse
import pandas as pd
from tqdm import tqdm
from src.univariate_analysis import univariate_analysis
from src.bivariate_analysis import bivariate_analysis
from src.multivariate_analysis import multivariate_analysis
from src.save_results import save_results
import os

def print_separator():
    """Print a colored separator for better CLI formatting."""
    print("\n" + "="*80 + "\n")


def main(input_file, output_dir, template_path=None):
    """Main function to perform EDA and save results to the output directory.

    :param input_file: Path to the input CSV file.
    :param output_dir: Directory where stats and charts will be saved.
    :param template_path: Optional path to the PowerPoint template.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        os.makedirs(f"{output_dir}/stats/")
        os.makedirs(f"{output_dir}/charts/")

    # Load data with tqdm progress bar
    print_separator()
    tqdm.write("\033[34mLoading data...\033[0m")  # Blue-colored text
    df = pd.read_csv(input_file)

    # Show a progress bar for the analysis
    tasks = [
        ("\033[92mUnivariate Analysis\033[0m", univariate_analysis),  # Green-colored task
        ("\033[93mBivariate Analysis\033[0m", bivariate_analysis),    # Yellow-colored task
        ("\033[95mMultivariate Analysis\033[0m", multivariate_analysis) # Magenta-colored task
    ]

    print_separator()
    tqdm.write("\033[34mStarting Exploratory Data Analysis (EDA)...\033[0m")

    for task_name, analysis_func in tqdm(
        tasks, 
        desc="Performing EDA", 
        ncols=100, 
        unit="task", 
        bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} {elapsed_s:.2f}s', 
        ascii=" |.|"):
        print_separator()
        tqdm.write(f"\n\033[94mStarting {task_name}...\033[0m")  # Blue for task start
        analysis_func(df, output_dir)

    # Save results and create presentation
    print_separator()
    tqdm.write("\033[34mSaving results and creating PowerPoint presentation...\033[0m")
    save_results(output_dir, template_path)
    tqdm.write("\033[92mPresentation created successfully!\033[0m")  # Green for success
    print_separator()


if __name__ == '__main__':
    # Initialize parser
    parser = argparse.ArgumentParser(description='Perform EDA and create a PowerPoint presentation.')

    # Add arguments
    parser.add_argument('input_file', type=str, help='Path to the input CSV file.')
    parser.add_argument('output_dir', type=str, help='Directory where output will be saved.')
    parser.add_argument('--template_path', type=str, default=None, help='Optional path to PowerPoint template.')

    # Parse arguments
    args = parser.parse_args()

    # Call main function with parsed arguments
    main(args.input_file, args.output_dir, args.template_path)
