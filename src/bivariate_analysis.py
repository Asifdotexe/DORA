import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def bivariate_analysis(df: pd.DataFrame, output_directory: str) -> None:
    """ This function performs a bivariate analysis on the given DataFrame, df, by creating scatter plots for each pair of numerical columns.
    
    :param df: The input DataFrame containing the data to be analyzed.
    :param output_directory: The directory where the analysis results will be saved.

    :returns: Nothing. Plots and saves the scatterplot in the given directory
    :rtype: None
    """
    charts_dir = os.path.join(output_directory, 'charts')
    os.makedirs(charts_dir, exist_ok=True)
    
    numerical_columns = df.select_dtypes(include=['float64', 'int64']).columns
    for index, column_1 in enumerate(numerical_columns):
        for column_2 in numerical_columns[index + 1:]:
            plt.figure(figsize=(10,6))
            sns.scatterplot(x=df[column_1], y=df[column_2])
            plt.title(f"Bivariate Analysis of {column_1} vs {column_2}")
            plt.savefig(f"{output_directory}/charts/bivariate_{column_1}_vs_{column_2}.png")
            plt.close()