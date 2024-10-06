import argparse
import pandas as pd
from src.univariate_analysis import univariate_analysis
from src.bivariate_analysis import bivariate_analysis
from src.multivariate_analysis import multivariate_analysis
from src.save_results import save_results
import os

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

    # Load data
    df = pd.read_csv(input_file)

    # Perform EDA
    univariate_analysis(df, output_dir)
    bivariate_analysis(df, output_dir)
    multivariate_analysis(df, output_dir)

    # Save results and create presentation
    save_results(output_dir, template_path)

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