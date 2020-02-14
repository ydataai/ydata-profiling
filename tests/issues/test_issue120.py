"""
Test for issue 120:
https://github.com/pandas-profiling/pandas-profiling/issues/120
"""
import pandas as pd

from pandas_profiling import ProfileReport


def test_issue_120(get_data_file):
    file_name = get_data_file(
        "pandas_profiling_bug.txt",
        "https://github.com/pandas-profiling/pandas-profiling/files/2386812/pandas_profiling_bug.txt",
    )
    df = pd.read_csv(file_name)

    report = ProfileReport(
        df,
        correlations={"cramers": {"calculate": False}},
        vars={"cat": {"check_composition": True}},
    )
    html = report.to_html()
    assert type(html) == str
    assert "<p class=h4>Dataset statistics</p>" in html
