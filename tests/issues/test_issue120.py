import pandas as pd
import pandas_profiling


# https://github.com/pandas-profiling/pandas-profiling/issues/120
def test_issue_120():
    df = pd.read_csv(
        "https://github.com/pandas-profiling/pandas-profiling/files/2386812/pandas_profiling_bug.txt"
    )

    report = df.profile_report(
        correlations={"cramers": False}, check_correlation_cramers=False
    )
    html = report.to_html()
    assert type(html) == str and '<p class="h2">Dataset info</p>' in html
