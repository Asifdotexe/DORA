"""
This module is responsible for generating visualisations for bivariate analysis
"""

import logging
import os

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from .styling import PRIMARY_COLOR, apply_custom_styling


def generate_plots(
    df: pd.DataFrame, target_column: str, charts_dir: str, config_params: dict
) -> list[str]:
    """
    Generates and save the plot for target-centric bi-variate plot

    :param df: Pandas dataframe containing the data to plot.
    :param charts_dir: Path to the directory you want to save the chart.
    :param config_params: Parameters defined by the user in the configuration file
    :returns: A list of paths pointing towards the plots
    """
    apply_custom_styling()
    # FIXME: Maybe this can be outside the function?
    # Check to determine if target centric analysis is needed
    if not config_params.get("target_centric"):
        logging.info(
            "Skipping the bivariate analysis as `target centric` is not enables"
        )
        return []

    plot_paths = []
    features = [column for column in df.columns if column != target_column]
    target_is_numeric = pd.api.types.is_numeric_dtype(df[target_column])

    for feature in features:
        plt.figure(figsize=(10, 6))
        feature_is_numeric = pd.api.types.is_numeric_dtype(df[feature])

        plot_generated = False
        # Numeric feature vs Numeric feature
        if feature_is_numeric and target_is_numeric:
            sns.scatterplot(data=df, x=feature, y=target_column, alpha=0.7)
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
            sns.boxplot(data=df, x=target_column, y=feature, color=PRIMARY_COLOR)
            plt.title(
                f"Distribution of {target_column.replace('_', ' ').title()} by {feature.replace('_', ' ').title()}",
                loc="left",
                fontsize=16,
                fontweight="bold",
            )
            plt.xlabel(target_column.replace("_", " ").title())
            plt.ylabel(feature.replace("_", " ").title())
            plot_generated = True

        if plot_generated:
            path = os.path.join(
                charts_dir, f"bivariate_{feature}_vs_{target_column}.png"
            )
            plt.tight_layout()
            plt.savefig(path)
            plt.close()
            plot_paths.append(os.path.relpath(path, charts_dir))
            logging.info(
                "Generated bivariate plot for %s vs %s", feature, target_column
            )

    return plot_paths
