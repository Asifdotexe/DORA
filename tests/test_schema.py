"""
Unit tests for schema validation.
"""

from pathlib import Path

import pytest
from pydantic import ValidationError

from dora.schema import Config


def test_config_max_categories_valid():
    """Test valid max_categories for Config."""
    config = Config(
        input_file=Path("dummy.csv"),
        output_dir=Path("output"),
        univariate_max_categories=1,
        bivariate_max_categories=10,
    )
    assert config.univariate_max_categories == 1
    assert config.bivariate_max_categories == 10


def test_config_univariate_max_categories_invalid():
    """Test invalid max_categories for Univariate (<= 0)."""
    with pytest.raises(ValidationError) as excinfo:
        Config(input_file=Path("dummy.csv"), output_dir=Path("output"), univariate_max_categories=0)
    assert "max_categories must be greater than 0" in str(excinfo.value)

    with pytest.raises(ValidationError) as excinfo:
        Config(input_file=Path("dummy.csv"), output_dir=Path("output"), univariate_max_categories=-5)
    assert "max_categories must be greater than 0" in str(excinfo.value)


def test_config_bivariate_max_categories_invalid():
    """Test invalid max_categories for Bivariate (<= 0)."""
    with pytest.raises(ValidationError) as excinfo:
        Config(input_file=Path("dummy.csv"), output_dir=Path("output"), bivariate_max_categories=0)
    assert "max_categories must be greater than 0" in str(excinfo.value)
