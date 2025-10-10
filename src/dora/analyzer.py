"""
This module will orchestrate the analysis
"""

import logging
import os

import pandas as pd

from .plots import bivariate, multivariate, univariate
from .profiling import generate_profile
from .reporting.generator import create_report


class Analyzer:
    """
    Orchestrates the entire Exploratory data analysis process based on configuration.
    """

    def __init__(self, df: pd.DataFrame, config: dict):
        self.df = df
        self.config = config
        self.output_dir = self.config["output_dir"]
        self.charts_dir = os.path.join(self.output_dir, "charts")
        self.report_data = {"title": self.config.get("report_title", "EDA Report")}

        # To keep our project tidy, we'll create dedicated folders for our outputs right away.
        # This prevents clutter and makes the final report easy to find.
        os.makedirs(self.charts_dir, exist_ok=True)

    def run(self):
        """
        Executes the analysis pipeline defined in the config.
        This is the main conductor, stepping through the user's chosen analysis
        plan and running each part in order.
        """
        pipeline = self.config.get("analysis_pipeline", [])

        for step in pipeline:
            step_name = list(step.keys())[0]
            params = step[step_name]

            # We only run the steps that the user has explicitly enabled in the config.
            # This makes the tool flexible and respects the user's choices.
            if params and params.get("enabled", False):
                logging.info("--- Running Step: %s ---", step_name.capitalize())
                if step_name == "profile":
                    self._run_profiling()
                elif step_name == "univariate":
                    self._run_univariate(params)
                elif step_name == "bivariate":
                    self._run_bivariate(params)
                elif step_name == "multivariate":
                    self._run_multivariate(params)

        # After all the analysis is done, we compile everything into a
        # beautiful, easy-to-read report.
        self._generate_report()

    def _run_profiling(self):
        # This step gives us a quick summary of the dataset's health and structure.
        profile_results = generate_profile(self.df)
        self.report_data["profile"] = profile_results

    def _run_univariate(self, params: dict):
        # By looking at columns one by one, we can understand their individual characteristics.
        univariate_plots = univariate.generate_plots(self.df, self.charts_dir, params)
        self.report_data["univariate_plots"] = univariate_plots

    def _run_bivariate(self, params: dict):
        # Now we start looking for connections. If the user has a specific goal (a target variable),
        # this is where we explore how other features might influence it.
        target = self.config.get("target_variable")

        # It's important to check if a target was actually provided.
        # Running this analysis without one wouldn't make sense, so we'll skip it.
        if params.get("target_centric") and not target:
            logging.warning(
                "Bivariate 'target_centric' is true, but no 'target_variable' is defined. Skipping."
            )
            return

        bivariate_plots = bivariate.generate_plots(
            self.df, target, self.charts_dir, params
        )
        self.report_data["bivariate_plots"] = bivariate_plots

    def _run_multivariate(self, params: dict):
        # This is where we see how numerical features interact with each other.
        # The correlation matrix is a powerful tool to spot these broader relationships at a glance.
        multivariate_plots = multivariate.generate_plots(
            self.df, self.charts_dir, params
        )
        self.report_data["multivariate_plots"] = multivariate_plots

    def _generate_report(self):
        # We take all the charts and insights we've gathered and collate them into a single HTML report.
        logging.info("--- Generating HTML Report ---")
        create_report(self.report_data, self.output_dir)
