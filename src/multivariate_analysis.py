import os
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from tqdm import tqdm
import logging

# Configure logging for this module
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

sns.set_style('whitegrid')

def multivariate_analysis(df: pd.DataFrame, output_directory: str) -> None:
    """Perform multivariate analysis on the DataFrame and save a correlation heatmap.

    :param df: The input DataFrame containing the data to be analyzed.
    :param output_directory: The directory where the analysis results will be saved.
    :raises ValueError: If no numeric data is available for correlation analysis.
    """
    charts_dir = os.path.join(output_directory, 'charts')
    os.makedirs(charts_dir, exist_ok=True)

    df_numeric = df.select_dtypes(include=['float64', 'int64'])
    if df_numeric.empty:
        logging.error("No numeric data available for correlation analysis.")
        raise ValueError("No numeric data available for correlation analysis.")

    # logging.info("Starting multivariate analysis...")
    
    # Plot correlation matrix
    # This section creates a heatmap for the correlation matrix of numeric columns.
    # A mask is used to hide the upper triangle of the matrix since the correlation 
    # values are symmetrical and we only need the lower half for visualization.
    with tqdm(total=2, desc="\033[94mMultivariate Analysis\033[0m", ncols=100, unit="step", colour='#008000') as pbar:
        plt.figure(figsize=(12, 8))
        mask = np.triu(np.ones_like(df_numeric.corr(), dtype=bool))  # Mask for upper triangle
        cmap = sns.diverging_palette(230, 20, as_cmap=True)  # Color map for heatmap
        
        # Generate heatmap
        sns.heatmap(df_numeric.corr(), annot=True, mask=mask, cmap=cmap)
        plt.title('Multivariate Analysis - Correlation Matrix')
        plt.savefig(f"{charts_dir}/correlation_matrix.png")
        plt.close()
        
        pbar.update(1)  # Update progress bar after generating heatmap
    # logging.info("Completed multivariate analysis.")
