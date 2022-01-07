"""
Test for the visualization functionality  
"""
import pandas as pd

from pandas_profiling import ProfileReport
from pandas_profiling.utils.cache import cache_file

test_data = pd.DataFrame([1, 2, 3])

matplotlib_colors = {"gold": "#ffd700", "b": "#0000ff", "#FF796C": "#ff796c"}

def test_report_with_custom_pie_chart_colors():
    profile = ProfileReport(df=test_data,
        progress_bar=False,
        samples=None,
        correlations=None,
        missing_diagrams=None,
        duplicates=None,
        interactions=None,
    )
    profile.config.plot.pie.colors = list(matplotlib_colors.keys())
    
    html_report = profile.to_html()
    for c, hex_code in matplotlib_colors.items():
        assert "fill: {}".format(hex_code) in html_report, f"Missing color code of {c}"
