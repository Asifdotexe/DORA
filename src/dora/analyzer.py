"""
This module will orchestrate the analysis
"""

import logging
import os
from typing import Any

import pandas as pd

from .plots import bivariate, multivariate, univariate
from .profiling import generate_profile
from .reporting.generator import create_report
from .schema import Config

logger = logging.getLogger(__name__)


def run_analysis(df: pd.DataFrame, config: Config):
    """
    Executes the analysis pipeline defined in the config.
    """
    output_dir = config.output_dir
    charts_dir = os.path.join(output_dir, "charts")
    report_data: dict[str, Any] = {"title": config.report_title}

    os.makedirs(charts_dir, exist_ok=True)

    if config.profile_enabled:
        logger.info("--- Running Step: Profile ---")
        report_data["profile"] = generate_profile(df)

    if config.univariate_enabled:
        logger.info("--- Running Step: Univariate ---")
        params = {"plot_types": config.univariate_plot_types, "max_categories": config.univariate_max_categories}
        report_data["univariate_plots"] = univariate.generate_plots(df, charts_dir, params)

    if config.bivariate_enabled:
        logger.info("--- Running Step: Bivariate ---")
        target = config.target_variable
        if config.bivariate_target_centric and not target:
            logger.warning("Bivariate 'target_centric' is true, but no 'target_variable' is defined. Skipping.")
        elif target:
            params = {
                "target_centric": config.bivariate_target_centric,
                "max_categories": config.bivariate_max_categories,
            }
            report_data["bivariate_plots"] = bivariate.generate_plots(df, target, charts_dir, params)

    if config.multivariate_enabled:
        logger.info("--- Running Step: Multivariate ---")
        params = {"correlation_cols": config.multivariate_correlation_cols}
        report_data["multivariate_plots"] = multivariate.generate_plots(df, charts_dir, params)

    logger.info("--- Generating HTML Report ---")
    create_report(report_data, output_dir)
