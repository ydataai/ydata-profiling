"""
Test for issue 51:
https://github.com/pandas-profiling/pandas-profiling/issues/51
"""
import numpy as np
import pandas as pd

import pandas_profiling


def test_issue51(get_data_file):
    # Categorical has empty ('') value
    file_name = get_data_file(
        "buggy1.pkl",
        "https://raw.githubusercontent.com/adamrossnelson/HelloWorld/master/sparefiles/buggy1.pkl",
    )

    df = pd.read_pickle(str(file_name))

    report = df.profile_report(
        title="Pandas Profiling Report", progress_bar=False, explorative=True
    )
    assert (
        "<title>Pandas Profiling Report</title>" in report.to_html()
    ), "Profile report should be generated."


def test_issue51_similar():
    df = pd.DataFrame(
        {
            "test": ["", "hoi", None],
            "blest": [None, "", "geert"],
            "bert": ["snor", "", None],
        }
    )

    report = df.profile_report(
        title="Pandas Profiling Report", progress_bar=False, explorative=True
    )
    report.set_variable("vars.num.low_categorical_threshold", 0)
    # FIXME: assert correlation values
    # print(report.get_description()["correlations"])

    assert (
        "<title>Pandas Profiling Report</title>" in report.to_html()
    ), "Profile report should be generated."


def test_issue51_empty():
    df = pd.DataFrame(
        {
            "test": ["", "", "", "", ""],
            "blest": ["", "", "", "", ""],
            "bert": ["", "", "", "", ""],
        }
    )

    report = df.profile_report(
        title="Pandas Profiling Report",
        progress_bar=False,
        explorative=True,
    )
    report.set_variable("vars.num.low_categorical_threshold", 0)

    assert (
        "cramers" not in report.get_description()["correlations"]
        or (
            report.get_description()["correlations"]["cramers"].values
            == np.ones((3, 3))
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

    report = df.profile_report(
        title="Pandas Profiling Report", progress_bar=False, explorative=True
    )
    report.set_variable("vars.num.low_categorical_threshold", 0)

    assert (
        report.get_description()["correlations"]["cramers"].values == np.ones((3, 3))
    ).all()
