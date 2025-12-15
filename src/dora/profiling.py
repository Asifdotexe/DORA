"""
This module is responsible for performing detailed, column-by-column data profiling.
It generates not just statistics, but also miniature "sparkline" plots for visual summaries.
"""

import base64
import io

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from .plots.styling import PRIMARY_BLUE, apply_custom_styling


def _create_sparkline(series: pd.Series) -> str:
    """
    Generates a tiny, minimalist histogram (a sparkline) for a numerical series
    and returns it as a Base64 encoded string.
    """
    apply_custom_styling()
    plt.figure(figsize=(4, 0.75))
    sns.histplot(series, color=PRIMARY_BLUE, legend=False)
    plt.gca().set_axis_off()
    plt.margins(0)
    plt.tight_layout(pad=0)
    buffer = io.BytesIO()
    plt.savefig(buffer, format="png", dpi=90, transparent=True)
    plt.close()
    buffer.seek(0)
    b64_string = base64.b64encode(buffer.read()).decode("utf-8")
    return b64_string


def generate_profile(df: pd.DataFrame, max_sparklines: int = 100) -> dict:
    """
    Performs data profiling on a given dataframe, generating stats and sparklines for each column.

    :param df: Pandas dataframe containing data
    :param max_sparklines: Maximum number of sparklines to generate (default: 100)
    :returns: Dictionary containing detailed profiling information for each column.
    """
    column_profiles = []
    numeric_cols_count = 0

    for column in df.columns:
        col_series = df[column]
        profile_data = {"name": column}

        if pd.api.types.is_numeric_dtype(col_series):
            stats = {
                "mean": col_series.mean(),
                "median": col_series.median(),
                "std": col_series.std(),
                "min": col_series.min(),
                "max": col_series.max(),
            }
            profile_data["type"] = "Numerical"
            profile_data["stats"] = stats

            # Only generate sparkline if under the limit
            if numeric_cols_count < max_sparklines:
                profile_data["sparkline_base64"] = _create_sparkline(col_series)
                numeric_cols_count += 1
            else:
                profile_data["sparkline_base64"] = None
        else:
            stats = {
                "unique_values": col_series.nunique(),
                "top_value": (
                    col_series.mode().iloc[0] if not col_series.mode().empty else "N/A"
                ),
            }
            top_5 = col_series.value_counts().nlargest(5)
            stats["top_5_counts"] = top_5.to_dict()
            stats["top_5_max_count"] = top_5.max() if not top_5.empty else 0
            profile_data["type"] = "Categorical"
            profile_data["stats"] = stats

        column_profiles.append(profile_data)

    # We find the missing values and convert the resulting DataFrame to an HTML string here.
    # If there are no missing values, this string will be empty.
    #
    # TODO: Add percentage missing values to the stats dictionary
    missing_df = pd.DataFrame(df.isnull().sum(), columns=["missing_count"]).query(
        "missing_count > 0"
    )
    missing_values_html = (
        missing_df.to_html(classes="table", border=0, index=True)
        if not missing_df.empty
        else None
    )

    final_profile = {
        "dataset_shape": df.shape,
        "column_profiles": column_profiles,
        # We pass the pre-rendered HTML (or None) to the template.
        "missing_values_html": missing_values_html,
    }

    return final_profile
