"""
Test for issue 587:
https://github.com/pandas-profiling/pandas-profiling/issues/587
"""
import pandas as pd

import pandas_profiling
from pandas_profiling.model.base import is_numeric


def test_issue587():
    # Minimal reproducible code
    series = pd.Series([1, None], dtype="Int64")
    series_description = get_counts(series)
    assert is_numeric(series, series_description) == True
