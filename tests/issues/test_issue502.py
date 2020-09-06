"""
Test for issue 502:
https://github.com/pandas-profiling/pandas-profiling/issues/502
"""
import pandas as pd

from pandas_profiling.model.summary import describe_1d


def test_issue502(summarizer, typeset):
    series = pd.Series([1, 2, 3, 4, 5], dtype=pd.Int64Dtype())

    result = describe_1d(series, summarizer, typeset)
    assert result["min"] == 1
    assert result["max"] == 5


def test_issue502_missing(summarizer, typeset):
    series = pd.Series([1, 2, 3, 4, 5, None], dtype=pd.Int64Dtype())

    result = describe_1d(series, summarizer, typeset)
    assert result["min"] == 1
    assert result["max"] == 5
