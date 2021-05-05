"""
Test for issue XXX:
https://github.com/pandas-profiling/pandas-profiling/issues/XXX
"""
import pandas as pd
import pytest

from pandas_profiling import ProfileReport


@pytest.mark.skip()
def test_issueXXX():
    # Minimal reproducible code
    df = pd.read_csv("<file>")

    report = ProfileReport(df)
    _ = report.description_set
