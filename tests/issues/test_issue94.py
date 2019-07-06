"""
Test for issue 94:
https://github.com/pandas-profiling/pandas-profiling/issues/94

Test based on:
https://stackoverflow.com/questions/52926527/pandas-profiling-1-4-1-throws-zerodivisionerror-for-valid-data-set-which-pandas
"""
from pathlib import Path

import pandas as pd

import pandas_profiling


def test_issue94(tmpdir):
    file_path = Path(str(tmpdir)) / "issue94.csv"
    file_path.write_text(
        """CourseName
PHY
MATHS
MATHS
MATHS
PHY
PHY
PHY
CHEM
CHEM
CHEM"""
    )
    df = pd.read_csv(str(file_path), parse_dates=True)
    profile = pandas_profiling.ProfileReport(df, title="Pandas Profiling Report")
    assert "<title>Pandas Profiling Report</title>" in profile.to_html()
