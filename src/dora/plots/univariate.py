"""
This module is responsible for generating visualisations for univariate analysis
"""

import logging
from pathlib import Path
from typing import Union

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from .styling import PRIMARY_BLUE, apply_custom_styling


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
            plot_series = _handle_high_cardinality(df[column], max_cats)

            ax = sns.countplot(
                y=plot_series, order=plot_series.value_counts().index, color=PRIMARY_BLUE
            )
            plt.title(
                f"Frequency of {column.replace('_', ' ').title()}",
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


def _handle_high_cardinality(series: pd.Series, max_categories: int) -> pd.Series:
    """
    Truncates the number of categories in a series to the top K most frequent.
    Remaining categories are grouped into 'Other'.

    :param series: The categorical series to process.
    :param max_categories: The maximum number of unique categories to keep.
    :return: A modified series with high cardinality handled.
    :rtype: pd.Series
    """
    if series.nunique() <= max_categories:
        return series

    # Identify top K - 1 categories
    top_categories = series.value_counts().nlargest(max_categories - 1).index
    
    # Replace others with 'Other'
    # Use apply/where or standard replacement
    # Using apply for explicit handling, though isin + loc is faster usually.
    # For categorical dtype, we might need to add category 'Other' first.
    
    new_series = series.copy()
    if isinstance(new_series.dtype, pd.CategoricalDtype):
         if "Other" not in new_series.cat.categories:
             new_series = new_series.cat.add_categories("Other")
    
    # Using where: Replace values NOT in top_categories with 'Other'
    new_series = new_series.where(new_series.isin(top_categories), "Other")
    
    return new_series
