"""
This module is responsible for generating visualisations for univariate analysis
"""

import logging
import os

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def generate_plots(df: pd.DataFrame, charts_dir: str, config_params: dict) -> list:
    """
    Generates and save univariate plots.

    :param df: Pandas dataframe containing the data to plot.
    :param charts_dir: Path to the directory you want to save the chart.
    :param config_params: Parameters defined by the user in the configuration file
    """
    plot_paths = []
    numerical_columns = df.select_dtypes(include=["number"]).columns
    categorical_columns = df.select_dtypes(include=["object", "category"]).columns

    for column in numerical_columns:
        for plot_type in config_params.get("plot_type", {}).get("numerical", []):
            plt.figure(figsize=(10, 6))
            if plot_type == "histogram":
                sns.histplot(df[column], kde=True)
                plt.title(f"Histogram of {column}")
            elif plot_type == "boxplot":
                sns.boxplot(x=df[column])
                plt.title(f"Box Plot of {column}")

            path = os.path.join(charts_dir, f"univariate_{column}_{plot_type}.png")
            plt.savefig(path)
            plt.close()
            plot_paths.append(os.path.relpath(path, charts_dir))
            logging.info("Generated %s for %s", plot_type, column)

    for column in categorical_columns:
        if "barplot" in config_params.get("plot_types", {}).get("categorical", []):
            plt.figure(figsize=(10, 6))
            sns.countplot(y=df[column], order=df[column].value_counts().index)
            plt.title(f"Bar Plot of {column}")
            plt.tight_layout()
            path = os.path.join(charts_dir, f"univariate_{column}_barplot.png")
            plt.savefig(path)
            plt.close()
            plot_paths.append(os.path.relpath(path, charts_dir))
            logging.info("Generated barplot for %s", column)

    return plot_paths
