import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from tqdm import tqdm
import logging

# Configure logging for this module
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

sns.set_style('whitegrid')

def bivariate_analysis(df: pd.DataFrame, output_directory: str) -> None:
    """Perform bivariate analysis on the DataFrame and save scatter plots.

    :param df: The input DataFrame containing the data to be analyzed.
    :param output_directory: The directory where the analysis results will be saved.
    """
    charts_dir = os.path.join(output_directory, 'charts')
    os.makedirs(charts_dir, exist_ok=True)

    num_columns = df.select_dtypes(include=['float64', 'int64']).columns

    logging.info("Starting bivariate analysis...")
    # Loop through numeric columns
    # This loop iterates over all numeric columns in the DataFrame. For each column,
    # it creates scatter plots comparing the current column with every other column that comes after it.
    # This ensures we only plot unique pairs, avoiding redundancy.
    for i, column in tqdm(enumerate(num_columns), desc="Bivariate Analysis", ncols=100, unit="column"):
        # Compare current column with all subsequent numeric columns
        for col2 in num_columns[i + 1:]:
            plt.figure(figsize=(10, 6))
            sns.scatterplot(data=df, x=column, y=col2)
            plt.title(f'Bivariate Analysis: {column} vs {col2}')
            plt.savefig(f"{charts_dir}/bivariate_{column}_vs_{col2}.png")
            plt.close()
    logging.info("Completed bivariate analysis.")
