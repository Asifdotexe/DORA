"""
Unit tests for schema validation.
"""

import pytest
from pydantic import ValidationError

from dora.schema import (AnalysisStep, BivariateStep, ProfileStep,
                         UnivariateStep)


def test_analysis_step_valid_single_field():
    """Test that AnalysisStep accepts exactly one field."""
    # Profile only
    step = AnalysisStep(profile=ProfileStep())
    assert step.profile is not None
    assert step.univariate is None

    # Univariate only
    step = AnalysisStep(univariate=UnivariateStep())
    assert step.univariate is not None
    assert step.profile is None


def test_analysis_step_invalid_zero_fields():
    """Test that AnalysisStep raises error when no fields are provided."""
    with pytest.raises(ValidationError) as excinfo:
        AnalysisStep()
    assert "Exactly one analysis step must be provided" in str(excinfo.value)


def test_analysis_step_invalid_multiple_fields():
    """Test that AnalysisStep raises error when multiple fields are provided."""
    with pytest.raises(ValidationError) as excinfo:
        AnalysisStep(profile=ProfileStep(), univariate=UnivariateStep())
    assert "Exactly one analysis step must be provided" in str(excinfo.value)


def test_univariate_step_max_categories_valid():
    """Test valid max_categories for UnivariateStep."""
    step = UnivariateStep(max_categories=1)
    assert step.max_categories == 1
    step = UnivariateStep(max_categories=100)
    assert step.max_categories == 100


def test_univariate_step_max_categories_invalid():
    """Test invalid max_categories for UnivariateStep (<= 0)."""
    with pytest.raises(ValidationError) as excinfo:
        UnivariateStep(max_categories=0)
    assert "max_categories must be greater than 0" in str(excinfo.value)

    with pytest.raises(ValidationError) as excinfo:
        UnivariateStep(max_categories=-5)
    assert "max_categories must be greater than 0" in str(excinfo.value)


def test_bivariate_step_max_categories_valid():
    """Test valid max_categories for BivariateStep."""
    step = BivariateStep(max_categories=10)
    assert step.max_categories == 10


def test_bivariate_step_max_categories_invalid():
    """Test invalid max_categories for BivariateStep (<= 0)."""
    with pytest.raises(ValidationError) as excinfo:
        BivariateStep(max_categories=0)
    assert "max_categories must be greater than 0" in str(excinfo.value)
