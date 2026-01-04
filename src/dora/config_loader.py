import logging
from pathlib import Path

import yaml

from dora.schema import Config


def load_config(config_path: Path) -> Config:
    """
    Load and validate the YAML configuration file using Pydantic

    :param config_path: Path to the YAML configuration file
    :returns: A Config object containing the configurations
    """
    logging.info("Reading the configuration file from %s", config_path)
    with open(config_path, "r", encoding="utf-8") as file:
        config_dict = yaml.safe_load(file) or {}

    # Pydantic validation handles missing fields and types
    try:
        # Resolve paths relative to the config file location
        if "input_file" in config_dict:
            input_path = Path(config_dict["input_file"])
            if not input_path.is_absolute():
                # If relative, make it relative to the config file, not CWD
                resolved_path = (config_path.parent / input_path).resolve()
                config_dict["input_file"] = str(resolved_path)

        config = Config(**config_dict)
        logging.info("Configuration loaded and validated successfully")
        return config
    except Exception as e:
        logging.error(f"Configuration validation failed: {e}")
        raise ValueError(f"Invalid configuration: {e}")
