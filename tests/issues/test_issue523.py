"""
Test for issue 523:
https://github.com/ydataai/ydata-profiling/issues/XXX
"""
from dataclasses import asdict

import pandas as pd

from ydata_profiling import ProfileReport


def test_issue523():
    # https://github.com/pandas-dev/pandas/issues/33803

    data = [
        1871248,
        12522551,
        1489260,
        6657093,
        pd.NA,
        pd.NA,
        pd.NA,
        pd.NA,
        pd.NA,
        1489260,
        pd.NA,
        2468576,
    ]
    df = pd.DataFrame({"col": data}, dtype=pd.Int64Dtype())

    profile_report = ProfileReport(df, title="Test Report", progress_bar=False)
    assert len(asdict(profile_report.get_description())) > 0
