import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from tqdm import tqdm

sns.set_style('whitegrid')

def bivariate_analysis(df: pd.DataFrame, output_directory: str) -> None:
    """ This function performs a bivariate analysis on the given DataFrame.

    :param df: The input DataFrame containing the data to be analyzed.
    :param output_directory: The directory where the analysis results will be saved.
    """
    
    # Ensure the necessary directories exist
    charts_dir = os.path.join(output_directory, 'charts')
    os.makedirs(charts_dir, exist_ok=True)

    # Select numerical columns for pairplots and correlation analysis
    num_columns = df.select_dtypes(include=['float64', 'int64']).columns
    
    for i, column in tqdm(enumerate(num_columns), desc="Bivariate Analysis", ncols=100, unit="column", colour='#008000', total=len(num_columns)):
        # For each column, pair with all remaining columns
        for j, col2 in enumerate(num_columns[i + 1:]):
            plt.figure(figsize=(10, 6))
            sns.scatterplot(data=df, x=column, y=col2)
            plt.title(f'Bivariate Analysis: {column} vs {col2}')
            plt.savefig(f"{charts_dir}/bivariate_{column}_vs_{col2}.png")
            plt.close()
