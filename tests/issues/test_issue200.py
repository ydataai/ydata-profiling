"""
Test for issue 200:
https://github.com/pandas-profiling/pandas-profiling/issues/200
"""
import pandas as pd

from pandas_profiling import ProfileReport


def test_issue200():
    df = pd.DataFrame([0, 1, 2], columns=["a"], index=["0", "1", "2"])

    assert df.index.dtype == "object", "Index type should be 'object'"
    report = ProfileReport(df, title="String indices")
    assert (
        "<title>String indices</title>" in report.to_html()
    ), "Profile report should be generated."
