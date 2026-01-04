"""
Module for loading data from various file formats.
"""

import logging
from pathlib import Path

import pandas as pd


def read_data(file_path: Path) -> pd.DataFrame:
    """
    Reads a data file into a pandas DataFrame.

    :param file_path: Path to the file to be read.
    :returns: A pandas DataFrame containing the data from the file.
    """
    suffix = file_path.suffix.lower()

    try:
        if suffix == ".csv":
            return pd.read_csv(file_path)
        if suffix == ".xlsx":
            return pd.read_excel(file_path)
        if suffix == ".json":
            return pd.read_json(file_path)
        if suffix == ".parquet":
            return pd.read_parquet(file_path)

        raise ValueError(f"Unsupported file extension: {suffix}")

    except ValueError as e:
        logging.error(f"Error reading file: {e}")
        raise
    except Exception as e:
        logging.error(f"Unexpected error reading file {file_path}: {e}")
        raise
