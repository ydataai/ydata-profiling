import pandas as pd

from pandas_profiling import ProfileReport


def test_report_empty():
    """Integration test for report with empty df"""
    df = pd.DataFrame(columns=["A", "B", "C", "D"])

    report = ProfileReport(df)
    html = report.to_html()
    assert "<a class=anchor href=#missing>Missing values</a>" not in html
    assert "<a class=anchor href=#correlations>Correlations</a>" not in html
    assert "<a class=anchor href=#sample>Sample</a>" not in html
