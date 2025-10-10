"""
This module is responsible for performing basic data profiling
"""

import pandas as pd


def generate_profile(df: pd.DataFrame) -> dict:
    """
    Performing data profiling on a given dataframe

    :param df: Pandas dataframe containing data
    :returns: Dictionary containing profiling information
    """
    # To avoid type confusion that can cause errors with Mypy, we keep the results
    # of our analysis as DataFrames instead of converting them to dictionaries.
    # This preserves the rich type information that pandas-stubs needs for verification.
    descriptive_stats_df = df.describe(include="all")

    # We also create the missing values DataFrame directly here.
    missing_df = pd.DataFrame(df.isnull().sum(), columns=["missing_count"])
    missing_df = missing_df[missing_df["missing_count"] > 0]

    profile = {
        "dataset_shape": df.shape,
        "descriptive_stats_df": descriptive_stats_df,
        "missing_values_df": missing_df,
        "column_types": df.dtypes.astype(str).to_dict(),
    }

    return profile
