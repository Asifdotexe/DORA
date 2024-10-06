import os
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from tqdm import tqdm

sns.set_style('whitegrid')

def multivariate_analysis(df: pd.DataFrame, output_directory: str) -> None:
    """This function performs a multivariate analysis on the given DataFrame.

    :param df: The input DataFrame containing the data to be analyzed.
    :param output_directory: The directory where the analysis results will be saved.
    
    :returns: Nothing. Plots and saves the scatterplot in the given directory.
    :rtype: None
    """
    charts_dir = os.path.join(output_directory, 'charts')
    os.makedirs(charts_dir, exist_ok=True)

    # Filter out non-numeric columns
    df_numeric = df.select_dtypes(include=['float64', 'int64'])
    
    if df_numeric.empty:
        raise ValueError("No numeric data available for correlation analysis.")
    
    # Start tqdm progress bar with 2 steps: (1) Correlation matrix, (2) Saving the plot
    with tqdm(total=2, desc="Multivariate Analysis", ncols=100, unit="step", colour='#008000') as pbar:
        plt.figure(figsize=(12, 8))
        
        # Step 1: Generate correlation matrix
        mask = np.triu(np.ones_like(df_numeric.corr(), dtype=bool))
        cmap = sns.diverging_palette(230, 20, as_cmap=True)
        sns.heatmap(df_numeric.corr(), annot=True, mask=mask, cmap=cmap)
        plt.title('Multivariate Analysis - Correlation Matrix')
        pbar.update(1)  # Update progress bar after generating correlation matrix

        # Step 2: Save the correlation plot
        plt.savefig(f"{charts_dir}/correlation_matrix.png")
        plt.close()
        pbar.update(1)  # Update progress bar after saving the file
