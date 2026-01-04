"""
This module is responsible for generating visualisations for multivariate analysis
"""

import logging
from pathlib import Path
from typing import Union

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from .styling import apply_custom_styling


def generate_plots(
    df: pd.DataFrame, charts_dir: Union[str, Path], config_params: dict
) -> list[str]:
    """
    Generates and saves a correlation heatmap.

    :param df: Pandas dataframe containing the data to plot.
    :param charts_dir: Path to the directory you want to save the chart.
    :param config_params: Parameters defined by the user in the configuration file
    :returns: A list of paths pointing towards the plots
    """
    apply_custom_styling()

    charts_dir_path = Path(charts_dir)
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
    cmap = sns.diverging_palette(230, 20, as_cmap=True)
    sns.heatmap(corr, annot=True, fmt=".2f", cmap=cmap, linewidths=0.5)
    plt.title(
        "Correlation Matrix of Numerical Features",
        loc="left",
        fontsize=16,
        fontweight="bold",
    )
    plt.tight_layout()

    path = charts_dir_path / "multivariate_correlation_matrix.png"
    plt.savefig(path)
    plt.close()
    plot_paths.append(str(path.relative_to(charts_dir_path)))
    logging.info("Generated correlation matrix.")

    return plot_paths
