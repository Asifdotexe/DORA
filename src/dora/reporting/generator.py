"""
This module would be responsible to put together a HTML report
"""

import datetime
import os

import pandas as pd
from jinja2 import Environment, FileSystemLoader


def create_report(report_data: dict, output_dir: str) -> None:
    """
    Generates an HTML report from the analysis using the Jinja2 templates

    :param report_data: The report data that needs to be added to the report
    :param output_dir: Path to the location we want to save the report to
    """
    # pointing to the directory containing the html template
    # NOTE: Changing the template would mean verifying if the class names are the same.
    template_dir = os.path.join(os.path.dirname(__file__), "templates")

    # Creating a Jinja object here to hold all the configurations and process the template file
    # essentially a template manager and the loader param helps the manager look at the template it needs to manage
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template("report_template.html")

    # FIXME: This logic could be faulty, verify when report is generated
    if "profile" in report_data and report_data.get("profile"):
        # Check for and process missing values data
        if "missing_values" in report_data["profile"]:
            missing_df = pd.DataFrame.from_dict(
                report_data["profile"]["missing_values"],
                orient="index",
                columns=["missing_count"],
            )
            missing_df = missing_df[missing_df["missing_count"] > 0]
            report_data["profile"]["missing_values_html"] = missing_df.to_html(
                classes="table table-striped"
            )

        # FIXME: This logic could be faulty, verify when report is generated
        if "descriptive_stats" in report_data["profile"]:
            desc_stats_df = pd.DataFrame(report_data["profile"]["descriptive_stats"])
            report_data["profile"]["descriptive_stats_html"] = desc_stats_df.to_html(
                classes="table table-striped", float_format="%.2f"
            )

    # Generates timestamp for the time of report generation
    report_data["generation_time"] = datetime.datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    html_content = template.render(report_data)

    report_path = os.path.join(output_dir, "eda_report.html")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(html_content)
