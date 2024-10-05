import pandas as pd
from src.univariate_analysis import univariate_analysis
from src.bivariate_analysis import bivariate_analysis
from src.multivariate_analysis import multivariate_analysis
from src.save_results import save_results
import os

def main(input_file, output_dir):
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
    save_results(output_dir)

if __name__ == '__main__':
    input_file = '../data/insurance.csv'  # Change this to your input file
    output_dir = 'output/'
    main(input_file, output_dir)