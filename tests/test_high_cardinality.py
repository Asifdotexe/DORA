import pandas as pd
import pytest
from dora.plots.univariate import _handle_high_cardinality

def test_handle_high_cardinality_no_truncation():
    """Test that series is unchanged if unique values <= max_categories."""
    data = ["A", "B", "C", "A", "B"]
    series = pd.Series(data)
    result, truncated = _handle_high_cardinality(series, max_categories=5)
    
    pd.testing.assert_series_equal(result, series)
    assert truncated is False

def test_handle_high_cardinality_truncation():
    """Test that series is truncated correctly."""
    # Create data with 5 categories: A (5), B (4), C (3), D (2), E (1)
    data = ["A"]*5 + ["B"]*4 + ["C"]*3 + ["D"]*2 + ["E"]*1
    series = pd.Series(data)
    
    # Max categories = 3. Should keep top 2 (A, B) and group (C, D, E) into Other
    result, truncated = _handle_high_cardinality(series, max_categories=3)
    
    expected_counts = {"A": 5, "B": 4, "Other": 6} # 3+2+1 = 6
    result_counts = result.value_counts().to_dict()
    
    assert result_counts == expected_counts
    assert "Other" in result.values
    assert truncated is True

def test_handle_high_cardinality_categorical_dtype():
    """Test that categorical dtype is preserved and 'Other' is added."""
    data = ["A"]*5 + ["B"]*4 + ["C"]*3
    series = pd.Series(data, dtype="category")
    
    # Max = 2. Keep A (top 1), others -> Other
    result, truncated = _handle_high_cardinality(series, max_categories=2)
    
    assert isinstance(result.dtype, pd.CategoricalDtype)
    assert "Other" in result.cat.categories
    assert result.value_counts()["Other"] == 7 # B(4) + C(3)
    assert truncated is True

def test_handle_high_cardinality_invalid_input():
    """Test that ValueError is raised for invalid max_categories."""
    series = pd.Series(["A", "B"])
    with pytest.raises(ValueError, match="max_categories must be an integer greater than or equal to 1"):
        _handle_high_cardinality(series, max_categories=0)

def test_handle_high_cardinality_empty_series():
    """Test that empty series is handled correctly."""
    series = pd.Series([], dtype="object")
    result, truncated = _handle_high_cardinality(series, max_categories=5)
    assert result.empty
    assert truncated is False

def test_handle_high_cardinality_max_one():
    """Test edge case where max_categories is 1. All non-nulls should become 'Other'."""
    data = ["A", "B", "C"]
    series = pd.Series(data)
    result, truncated = _handle_high_cardinality(series, max_categories=1)
    
    assert (result == "Other").all()
    assert truncated is True
