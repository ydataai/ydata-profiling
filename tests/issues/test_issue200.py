"""
Test for issue 200:
https://github.com/ydataai/ydata-profiling/issues/200
"""
import pandas as pd

from ydata_profiling import ProfileReport


def test_issue200():
    df = pd.DataFrame([0, 1, 2], columns=["a"], index=["0", "1", "2"])

    assert df.index.dtype == "object", "Index type should be 'object'"
    report = ProfileReport(df, title="String indices", progress_bar=False, pool_size=1)
    assert (
        "<title>String indices</title>" in report.to_html()
    ), "Profile report should be generated."
