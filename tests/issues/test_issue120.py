"""
Test for issue 120:
https://github.com/pandas-profiling/pandas-profiling/issues/120
"""
import pandas as pd

from pandas_profiling import ProfileReport


def test_issue_120():
    df = pd.read_csv(
        "https://github.com/pandas-profiling/pandas-profiling/files/2386812/pandas_profiling_bug.txt"
    )

    report = ProfileReport(df, correlations={"cramers": {"calculate": False}})
    html = report.to_html()
    assert type(html) == str
    assert '<p class=h2>Dataset info</p>' in html
