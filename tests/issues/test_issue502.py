"""
Test for issue 502:
https://github.com/ydataai/ydata-profiling/issues/502
"""
import pandas as pd

from ydata_profiling.model.summary import describe_1d


def test_issue502(config, summarizer, typeset):
    series = pd.Series([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], dtype=pd.Int64Dtype())

    result = describe_1d(config, series, summarizer, typeset)
    assert result["min"] == 1
    assert result["max"] == 11


def test_issue502_missing(config, summarizer, typeset):
    series = pd.Series([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, None], dtype=pd.Int64Dtype())

    result = describe_1d(config, series, summarizer, typeset)
    assert result["min"] == 1
    assert result["max"] == 11
