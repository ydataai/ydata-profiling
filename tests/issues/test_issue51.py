"""
Test for issue 51:
https://github.com/ydataai/ydata-profiling/issues/51
"""
import numpy as np
import pandas as pd

from ydata_profiling import ProfileReport


def test_issue51(get_data_file):
    # Categorical has empty ('') value
    file_name = get_data_file(
        "buggy1.pkl",
        "https://raw.githubusercontent.com/adamrossnelson/HelloWorld/master/sparefiles/buggy1.pkl",
    )

    df = pd.read_pickle(str(file_name))

    report = ProfileReport(
        df, title="YData Profiling Report", progress_bar=False, explorative=True
    )
    assert (
        "<title>YData Profiling Report</title>" in report.to_html()
    ), "Profile report should be generated."


def test_issue51_similar():
    df = pd.DataFrame(
        {
            "test": ["", "hoi", None],
            "blest": [None, "", "geert"],
            "bert": ["snor", "", None],
        }
    )

    report = ProfileReport(
        df, title="YData Profiling Report", progress_bar=False, explorative=True
    )
    report.config.vars.num.low_categorical_threshold = 0
    # FIXME: assert correlation values (report.description_set["correlations"])

    assert (
        "<title>YData Profiling Report</title>" in report.to_html()
    ), "Profile report should be generated."


def test_issue51_empty():
    df = pd.DataFrame(
        {
            "test": ["", "", "", "", ""],
            "blest": ["", "", "", "", ""],
            "bert": ["", "", "", "", ""],
        }
    )

    report = ProfileReport(
        df,
        title="YData Profiling Report",
        progress_bar=False,
        explorative=True,
    )
    report.config.vars.num.low_categorical_threshold = 0

    assert (
        "cramers" not in report.get_description().correlations
        or (
            report.get_description().correlations["cramers"].values == np.ones((3, 3))
        ).all()
    )


def test_issue51_identical():
    df = pd.DataFrame(
        {
            "test": ["v1", "v1", "v1"],
            "blest": ["v1", "v1", "v1"],
            "bert": ["v1", "v1", "v1"],
        }
    )

    report = ProfileReport(
        df, title="YData Profiling Report", progress_bar=False, explorative=True
    )
    report.config.vars.num.low_categorical_threshold = 0
    # this should not return any correlation value as the variables are identical constants
    assert report.get_description().correlations == {}
