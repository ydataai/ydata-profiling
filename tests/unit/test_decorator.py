import pandas as pd

from ydata_profiling import ProfileReport


def test_decorator(get_data_file):
    people_example = get_data_file(
        "people_example.csv",
        "https://raw.githubusercontent.com/ydataai/coursera-ml/master/week-1/people-example.csv",
    )
    df = pd.read_csv(people_example)
    report = ProfileReport(
        df,
        title="Coursera Test Report",
        samples={"head": 20},
        missing_diagrams={"heatmap": False},
    )
    assert "Coursera Test Report" in report.to_html(), "Title is not found"
