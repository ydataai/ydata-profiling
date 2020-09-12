"""
Test for issue 249:
https://github.com/pandas-profiling/pandas-profiling/issues/249
"""
import pandas as pd

import pandas_profiling


def test_issue249():
    df = pd.DataFrame(data=[[1], [2]], index=["foo", 1], columns=["a"])
    report = df.profile_report(explorative=True)
    assert type(report.title) == str
    assert len(report.to_html()) > 0
