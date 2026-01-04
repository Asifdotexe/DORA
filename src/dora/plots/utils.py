"""
Utility functions for plotting.
"""

import pandas as pd


def handle_high_cardinality(
    series: pd.Series, max_categories: int
) -> tuple[pd.Series, bool]:
    """
    Truncates the number of categories in a series to the top K most frequent.
    Remaining categories are grouped into 'Other'.

    :param series: The categorical series to process.
    :param max_categories: The maximum number of unique categories to keep.
    :return: A tuple containing the modified series and a boolean indicating if truncation occurred.
    :raises ValueError: If max_categories is less than 1.
    """
    if max_categories < 1:
        raise ValueError("max_categories must be an integer greater than or equal to 1")

    if series.empty:
        return series.copy(), False

    # Return input if unique count is within limits and max_categories > 1 (if 1, we force 'Other' unless only 1 exists)
    # Actually if max_categories == 1, we only keep the top 1 (if any), rest is Other.
    # If there is already only 1 unique value, no truncation needed.
    if series.nunique() <= max_categories:
        return series.copy(), False

    truncation_occurred = True

    if max_categories == 1:
        top_categories = pd.Index([])
    else:
        # Identify top K - 1 categories
        top_categories = series.value_counts().nlargest(max_categories - 1).index

    # Replace others with 'Other'
    new_series = series.copy()
    if isinstance(new_series.dtype, pd.CategoricalDtype):
        if "Other" not in new_series.cat.categories:
            new_series = new_series.cat.add_categories("Other")

    # Using where: Replace values NOT in top_categories with 'Other'
    new_series = new_series.where(new_series.isin(top_categories), "Other")

    return new_series, truncation_occurred
