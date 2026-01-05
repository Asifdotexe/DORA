"""
Module for interacting with Kaggle API.
"""

import logging
import re
from pathlib import Path

import kagglehub
from rich import print as rprint
from rich.prompt import IntPrompt


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

        :param input_str: The input string (link) to extract the dataset ID from.
        :return: The extracted dataset ID.
        """
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
        logging.info("Downloading dataset %s", dataset_id)
        try:
            dataset_path = kagglehub.dataset_download(dataset_id)
            dataset_download_directory = Path(dataset_path)
        except RuntimeError as e:
            raise ValueError(f"Failed to download dataset: {e}") from e

        # Extracting file based on their extensions
        supported_extensions = [".csv", ".json", ".parquet", ".xlsx"]
        files = [
            file
            for file in dataset_download_directory.glob("**/*")
            if file.suffix.lower() in supported_extensions and file.is_file()
        ]

        if not files:
            raise ValueError("No supported files found in the downloaded dataset.")

        if len(files) == 1:
            return files[0]

        # Interactive selection for multiple files
        rprint(f"\n[cyan]Multiple data files found in {dataset_id}:[/cyan]")
        for i, file in enumerate(files):
            try:
                size_mb = file.stat().st_size / (1024 * 1024)
                rprint(f"[{i + 1}] {file.name} ({size_mb:.2f} MB)")
            except (OSError, PermissionError) as e:
                logging.warning("Could not stat file %s: %s", file.name, e)
                rprint(f"[{i + 1}] {file.name} (size unknown)")

        choice = IntPrompt.ask(
            "Select a file number", choices=[str(i + 1) for i in range(len(files))]
        )
        return files[choice - 1]
