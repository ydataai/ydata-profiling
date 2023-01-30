"""
Test for issue 249:
https://github.com/ydataai/ydata-profiling/issues/249
"""
import pandas as pd

from ydata_profiling import ProfileReport


def test_issue249():
    df = pd.DataFrame(data=[[1], [2]], index=["foo", 1], columns=["a"])
    report = ProfileReport(df, explorative=True, progress_bar=False)
    assert type(report.config.title) == str
    assert len(report.to_html()) > 0
