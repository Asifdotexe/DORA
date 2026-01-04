"""
This module is responsible for generating visualisations for bivariate analysis
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
from .utils import handle_high_cardinality


def generate_plots(
    df: pd.DataFrame,
    target_column: str,
    charts_dir: Union[str, Path],
    config_params: dict,
) -> list[str]:
    """
    Generates and save the plot for target-centric bi-variate plot

    :param df: Pandas dataframe containing the data to plot.
    :param charts_dir: Path to the directory you want to save the chart.
    :param config_params: Parameters defined by the user in the configuration file
    :returns: A list of paths pointing towards the plots
    """
    apply_custom_styling()

    # Check to determine if target centric analysis is needed
    if not config_params.get("target_centric"):
        logging.info(
            "Skipping the bivariate analysis as `target centric` is not enables"
        )
        return []

    charts_dir_path = Path(charts_dir)
    plot_paths = []
    features = [column for column in df.columns if column != target_column]
    target_is_numeric = pd.api.types.is_numeric_dtype(df[target_column])

    for feature in features:
        plt.figure(figsize=(10, 6))
        feature_is_numeric = pd.api.types.is_numeric_dtype(df[feature])

        plot_generated = False
        # Numeric feature vs Numeric feature
        if feature_is_numeric and target_is_numeric:
            sns.scatterplot(
                data=df, x=feature, y=target_column, alpha=0.6, color=PRIMARY_BLUE
            )
            plt.title(
                f"{target_column.replace('_', ' ').title()} vs. {feature.replace('_', ' ').title()}",
                loc="left",
                fontsize=16,
                fontweight="bold",
            )
            plt.xlabel(feature.replace("_", " ").title())
            plt.ylabel(target_column.replace("_", " ").title())
            plot_generated = True

        # Categorical Feature vs. Numeric Target
        elif not feature_is_numeric and target_is_numeric:
            max_cats = config_params.get("max_categories", 20)
            plot_series, truncated = handle_high_cardinality(df[feature], max_cats)

            # For boxplot we can pass vectors directly
            sns.boxplot(x=df[target_column], y=plot_series, color=PRIMARY_BLUE)

            title_text = f"Distribution of {target_column.replace('_', ' ').title()} by {feature.replace('_', ' ').title()}"
            if truncated:
                title_text += f"\n(Top {max_cats} categories)"

            plt.title(
                title_text,
                loc="left",
                fontsize=16,
                fontweight="bold",
            )
            plt.xlabel(target_column.replace("_", " ").title())
            plt.ylabel(feature.replace("_", " ").title())
            plot_generated = True

        if plot_generated:
            path = charts_dir_path / f"bivariate_{feature}_vs_{target_column}.png"
            plt.tight_layout()
            plt.savefig(path)
            plt.close()
            plot_paths.append(str(path.relative_to(charts_dir_path)))
            logging.info(
                "Generated bivariate plot for %s vs %s", feature, target_column
            )

    return plot_paths
