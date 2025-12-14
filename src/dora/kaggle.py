"""
Module for interacting with Kaggle API.
"""

import logging
import re
from pathlib import Path

import kagglehub


class KaggleHandler:
    """
    Class for interacting with kaggle via KaggleHub
    """

    @staticmethod
    def is_kaggle_url(input_str: str) -> bool:
        """
        Checks if the given URL is a valid Kaggle URL.

        :param input_str: The URL to check.
        :return: True if the URL is a valid Kaggle URL, False otherwise.
        """
        # Check for kaggle.com domain or owner/dataset format (simple heuristic)
        if "kaggle.com" in input_str:
            return True
        # Check if it looks like owner/dataset-name format
        # Must have exactly one "/" and not be an existing file or absolute path
        return (
            "/" in input_str
            and input_str.count("/") == 1
            and not Path(input_str).exists()
            and not input_str.startswith("/")
            and not input_str.startswith("http")
        )

    @staticmethod
    def extract_dataset_id(input_str: str) -> str:
        """
        Extract the 'owner/dataset-name' identifier from a Kaggle URL.
        """
        # NOTE: Updated from match to search pattern in the entire string
        match = re.search(r"kaggle\.com/datasets/([^/]+/[^/?]+)", input_str)
        if match:
            return match.group(1)
        return input_str

    @staticmethod
    def download_dataset(dataset_id: str) -> Path:
        """
        Download a Kaggle dataset from kagglehub and return the path to the downloaded file.

        :param dataset_id: The 'owner/dataset-name' identifier of the dataset to download.
        :return: The path to the downloaded file.
        """
        logging.info(f"Downloading dataset {dataset_id}")
        try:
            dataset_path = kagglehub.dataset_download(dataset_id)
            dataset_download_directory = Path(dataset_path)
        except RuntimeError as e:
            raise ValueError(f"Failed to download dataset: {e}") from e

        # Extracting file based on their extensions
        supported_extensions = [".csv", ".json", ".parquet", ".xlsx", ".xls"]
        files = [
            file
            for file in dataset_download_directory.glob("**/*")
            if file.suffix.lower() in supported_extensions and file.is_file()
        ]

        if not files:
            raise ValueError("No supported files found in the downloaded dataset.")

        # Pick the largest file by default
        # FIXME: This logic has its flaws and needs to be revised.
        main_file = max(files, key=lambda file: file.stat().st_size)
        return main_file
