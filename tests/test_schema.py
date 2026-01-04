"""
Unit tests for schema validation.
"""

import pytest
from pydantic import ValidationError

from dora.schema import AnalysisStep, ProfileStep, UnivariateStep


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
