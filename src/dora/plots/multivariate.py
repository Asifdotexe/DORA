"""
This module is responsible for generating visualisations for multivariate analysis
"""

import logging
import os

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def generate_plots(df: pd.DataFrame, charts_dir: str, config_params: dict) -> list[str]:
    """
    Generates and saves a correlation heatmap.

    :param df: Pandas dataframe containing the data to plot.
    :param charts_dir: Path to the directory you want to save the chart.
    :param config_params: Parameters defined by the user in the configuration file
    :returns: A list of paths pointing towards the plots
    """
    plot_paths = []
    cols = config_params.get("correlation_cols")

    if not cols:
        # If no columns specified, use all numeric
        df_numeric = df.select_dtypes(include=["number"])
    else:
        df_numeric = df[cols]

    if df_numeric.shape[1] < 2:
        logging.warning(
            "Not enough numeric columns for a correlation matrix. Skipping."
        )
        return []

    plt.figure(figsize=(12, 10))
    corr = df_numeric.corr()
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm")
    plt.title("Correlation Matrix")
    plt.tight_layout()

    path = os.path.join(charts_dir, "multivariate_correlation_matrix.png")
    plt.savefig(path)
    plt.close()
    plot_paths.append(os.path.relpath(path, charts_dir))
    logging.info("Generated correlation matrix.")

    return plot_paths
