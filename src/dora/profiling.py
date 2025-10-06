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
    profile = {
        "dataset_shape": df.shape,
        "missing_values": df.isnull().sum().to_dict(),
        "descriptive_statistics": df.describe(include="all").to_dict(),
        "column_types": df.dtypes.astype(str).to_dict(),
    }

    return profile
