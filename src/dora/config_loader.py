"""
This module helps to load and validate the configuration file
"""

import logging
from pathlib import Path

import yaml


def load_config(config_path: Path) -> dict:
    """
    Load and validate the YAML configuration file

    :param config_path: Path to the YAML configuration file
    :returns: A dictionary containing the configurations
    """
    logging.info("Reading the configuration file from %s", config_path)
    with open(config_path, "r", encoding="utf-8") as file:
        config = yaml.safe_load(file) or {}

    # validation
    if "input_file" not in config or "output_dir" not in config:
        raise ValueError("Config file must contain 'input_file' and 'output_dir'.")

    logging.info("Configuration loaded successfully")
    return config
