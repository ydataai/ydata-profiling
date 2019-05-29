import pandas as pd
from IPython.lib.display import IFrame

import pandas_profiling


def test_decorator():
    df = pd.read_csv(
        "https://raw.githubusercontent.com/oncletom/coursera-ml/master/week-1/people-example.csv"
    )
    report = df.profile_report(
        title="Coursera Test Report",
        samples={"head": 20},
        missing_diagrams={"heatmap": False, "dendrogram": False},
    )
    assert "Coursera Test Report" in report.to_html(), "Title is not found"
