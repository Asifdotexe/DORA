import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from tqdm import tqdm
import logging

# Configure logging for this module
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

sns.set_style('whitegrid')

def univariate_analysis(df: pd.DataFrame, output_directory: str) -> str:
    """This function performs a univariate analysis on the given DataFrame.

    :param df: The input DataFrame containing the data to be analyzed.
    :param output_directory: The directory where the analysis results will be saved.

    :returns: The path to the file containing the statistical summary of the DataFrame.
    :rtype: str
    """
    
    # Ensure the necessary directories exist
    # Creating directories for statistics and charts if they do not already exist.
    stats_dir = os.path.join(output_directory, 'stats')
    charts_dir = os.path.join(output_directory, 'charts')
    
    os.makedirs(stats_dir, exist_ok=True)
    os.makedirs(charts_dir, exist_ok=True)
    
    # Save statistical summary
    stats = df.describe(include="all")
    stats_file = f"{stats_dir}/univariate_analysis.txt"
    
    # Write the statistical summary to a text file
    stats.to_string(open(stats_file, 'w'))
    logging.info("Statistical summary saved to %s", stats_file)

    # Create charts for each column with a progress bar
    columns = df.select_dtypes(include=['float64', 'int64', 'object']).columns
    
    # Loop through each column for univariate analysis
    # This loop iterates over all relevant columns in the DataFrame.
    # Depending on the data type, it generates either a count plot (for categorical data)
    # or a histogram with a kernel density estimate (for numerical data).
    for column in tqdm(columns, desc="Univariate Analysis", ncols=100, unit="column", colour='#008000'):
        plt.figure(figsize=(10, 6))

        # Check the data type of the column to determine the appropriate plot
        if df[column].dtype == 'object':
            # Count plot for categorical data
            sns.countplot(data=df, y=column)
        else:
            # Histogram and KDE for numerical data
            sns.histplot(data=df, x=column, kde=True)

        plt.title(f'Univariate Analysis of {column}')
        plt.savefig(f"{charts_dir}/univariate_{column}.png")
        plt.close()
        logging.info("Generated plot for %s", column)

    logging.info("Univariate analysis completed successfully.")
    return stats_file
