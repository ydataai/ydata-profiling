"""
Test for issue 587:
https://github.com/pandas-profiling/pandas-profiling/issues/587
"""
import pandas as pd
import pytest

from pandas_profiling.model.base import get_counts, is_numeric


@pytest.mark.skipif(
    int(pd.__version__.split(".")[0]) < 1, reason="requires pandas 1 or higher"
)
def test_issue587():
    # Minimal reproducible code
    series = pd.Series([1, None], dtype="Int64")
    series_description = get_counts(series)
    assert is_numeric(series, series_description) == True
