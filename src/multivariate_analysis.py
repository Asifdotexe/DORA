import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def multivariate_analysis(df: pd.DataFrame, output_directory: str) -> None:
    """This function performs a multivariate analysis on the given DataFrame.

    :param df: The input DataFrame containing the data to be analyzed.
    :param output_directory: The directory where the analysis results will be saved.
    
    :returns: Nothing. Plots and saves the scatterplot in the given directory
    :rtype: None
    """
    charts_dir = os.path.join(output_directory, 'charts')
    os.makedirs(charts_dir, exist_ok=True)
    
    # Filter out non-numeric columns
    numeric_df = df.select_dtypes(include=['float64', 'int64'])
    
    if numeric_df.empty:
        raise ValueError("No numeric data available for correlation analysis.")
    
    plt.figure(figsize=(12,8))
    sns.heatmap(df.corr(), annot=True, cmap='coolwarm')
    plt.title('Multivariate Analysis - Correlation Matrix')
    plt.savefig("f{output_directory}/charts/correlation_matrix.png")
    plt.close()