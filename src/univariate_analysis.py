import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def univariate_analysis(df: pd.DataFrame, output_directory: str) -> str:
    """ This function performs a univariate analysis on the given DataFrame.

    :param df: The input DataFrame containing the data to be analyzed.
    :param output_directory: The directory where the analysis results will be saved.

    :returns: The path to the file containing the statistical summary of the DataFrame.
    :rtype: str
    """
    
    # Ensure the necessary directories exist
    stats_dir = os.path.join(output_directory, 'stats')
    charts_dir = os.path.join(output_directory, 'charts')
    
    os.makedirs(stats_dir, exist_ok=True)
    os.makedirs(charts_dir, exist_ok=True)
    
    stats = df.describe(include="all")
    stats_file = f"{output_directory}/stats/univariate_analysis.txt"
    stats.to_string(open(stats_file, 'w'))

    for column in df.select_dtypes(include=['float64','int64','object']):
        plt.figure(figsize=(10,6))
        if df[column].dtype == 'object':
            sns.countplot(data=df, y=column)
        else:
            sns.histplot(data=df, x=column, kde=True)

        plt.title(f'Univariate Analysis of {column}')
        plt.savefig(f"{output_directory}/charts/univariate_{column}.png")
        plt.close()

    return stats_file