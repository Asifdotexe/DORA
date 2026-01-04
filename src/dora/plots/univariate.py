"""
This module is responsible for generating visualisations for univariate analysis
"""

# pylint: disable=wrong-import-position

import logging
from pathlib import Path
from typing import Union

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from .styling import PRIMARY_BLUE, apply_custom_styling
from .utils import handle_high_cardinality


def generate_plots(
    df: pd.DataFrame, charts_dir: Union[str, Path], config_params: dict
) -> list[str]:
    """
    Generates and save univariate plots.

    :param df: Pandas dataframe containing the data to plot.
    :param charts_dir: Path to the directory you want to save the chart.
    :param config_params: Parameters defined by the user in the configuration file
    :returns: A list of paths pointing towards the plots
    """
    apply_custom_styling()

    charts_dir_path = Path(charts_dir)
    plot_paths = []
    numerical_columns = df.select_dtypes(include=["number"]).columns
    categorical_columns = df.select_dtypes(include=["object", "category"]).columns

    # Generates the histogram and boxplots using the numerical data specified by the user in the config.yaml file
    for column in numerical_columns:
        for plot_type in config_params.get("plot_types", {}).get("numerical", []):
            plt.figure(figsize=(10, 6))
            if plot_type == "histogram":
                sns.histplot(df[column], color=PRIMARY_BLUE)
                plt.title(
                    f"Distribution of {column.replace('_', ' ').title()}",
                    loc="left",
                    fontsize=16,
                    fontweight="bold",
                )
                plt.xlabel(column.replace("_", " ").title())
                plt.ylabel("Frequency")
                plt.grid()

            elif plot_type == "boxplot":
                sns.boxplot(x=df[column], color=PRIMARY_BLUE)
                plt.title(
                    f"Box Plot for {column.replace('_', ' ').title()}",
                    loc="left",
                    fontsize=16,
                    fontweight="bold",
                )
                plt.xlabel(column.replace("_", " ").title())

            path = charts_dir_path / f"univariate_{column}_{plot_type}.png"
            plt.tight_layout()
            plt.savefig(path)
            plt.close()
            plot_paths.append(str(path.relative_to(charts_dir_path)))
            logging.info("Generated %s for %s", plot_type, column)

    # Generates barplot using the categorical data specified by the user in the config.yaml file
    for column in categorical_columns:
        if "barplot" in config_params.get("plot_types", {}).get("categorical", []):
            plt.figure(figsize=(10, 6))

            # Handle high cardinality
            max_cats = config_params.get("max_categories", 20)
            plot_series, truncated = handle_high_cardinality(df[column], max_cats)

            ax = sns.countplot(
                y=plot_series,
                order=plot_series.value_counts().index,
                color=PRIMARY_BLUE,
            )

            title_text = f"Frequency of {column.replace('_', ' ').title()}"
            if truncated:
                title_text += f"\n(Top {max_cats} categories)"

            plt.title(
                title_text,
                loc="left",
                fontsize=16,
                fontweight="bold",
            )
            plt.tight_layout()
            # We remove the y-axis label as it's redundant with the category names.
            plt.ylabel("")
            plt.xlabel("Count")
            for p in ax.patches:
                ax.annotate(
                    f"{int(p.get_width())}",
                    (p.get_width(), p.get_y() + p.get_height() / 2.0),
                    ha="left",
                    va="center",
                    xytext=(5, 0),
                    textcoords="offset points",
                )

            path = charts_dir_path / f"univariate_{column}_barplot.png"
            plt.savefig(path)
            plt.close()
            plot_paths.append(str(path.relative_to(charts_dir_path)))
            logging.info("Generated barplot for %s", column)

    return plot_paths
