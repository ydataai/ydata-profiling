import pandas as pd

import pandas_profiling


def test_decorator(get_data_file):
    people_example = get_data_file(
        "people_example.csv",
        "https://raw.githubusercontent.com/oncletom/coursera-ml/master/week-1/people-example.csv",
    )
    df = pd.read_csv(people_example)
    report = df.profile_report(
        title="Coursera Test Report",
        samples={"head": 20},
        missing_diagrams={"heatmap": False, "dendrogram": False},
    )
    assert "Coursera Test Report" in report.to_html(), "Title is not found"
