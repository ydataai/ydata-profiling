"""
Test for issue 51:
https://github.com/pandas-profiling/pandas-profiling/issues/51
"""
import numpy as np
import pandas as pd

import pandas_profiling

# FIXME: correlations can be computed stand alone to speed up tests
from pandas_profiling.config import config


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
    config["vars"]["num"]["low_categorical_threshold"] = 0
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
    # FIXME: assert correlation values
    # print(report.get_description()["correlations"])

    assert (
        "<title>Pandas Profiling Report</title>" in report.to_html()
    ), "Profile report should be generated."


def test_issue51_empty():
    config["vars"]["num"]["low_categorical_threshold"] = 0
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

    assert (
        "cramers" not in report.get_description()["correlations"]
        or (
            report.get_description()["correlations"]["cramers"].values
            == np.ones((3, 3))
        ).all()
    )


def test_issue51_identical():
    config["vars"]["num"]["low_categorical_threshold"] = 0
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
    assert (
        report.get_description()["correlations"]["cramers"].values == np.ones((3, 3))
    ).all()
