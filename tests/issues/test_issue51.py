"""
Test for issue 51:
https://github.com/pandas-profiling/pandas-profiling/issues/51
"""
from pathlib import Path

import pandas as pd
import pandas_profiling
import requests

import numpy as np


def test_issue51(get_data_file):
    # Categorical has empty ('') value
    file_name = get_data_file(
        "buggy1.pkl",
        "https://raw.githubusercontent.com/adamrossnelson/HelloWorld/master/sparefiles/buggy1.pkl",
    )

    df = pd.read_pickle(str(file_name))

    report = df.profile_report(title="Pandas Profiling Report")
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

    report = df.profile_report(title="Pandas Profiling Report")

    assert (
        "<title>Pandas Profiling Report</title>" in report.to_html()
    ), "Profile report should be generated."


def test_issue51_mixed():
    df = pd.DataFrame(
        {
            "test": ["", "hoi", None],
            "blest": [None, "", "geert"],
            "bert": ["snor", "", np.nan],
        }
    )
    report = df.profile_report(title="Pandas Profiling Report")

    assert (
        "data-toggle=tab>Recoded</a>" in report.to_html()
    ), "Recoded should be present"


def test_issue51_empty():
    df = pd.DataFrame(
        {"test": ["", "", ""], "blest": ["", "", ""], "bert": ["", "", ""]}
    )

    report = df.profile_report(title="Pandas Profiling Report")

    assert (
        "<title>Pandas Profiling Report</title>" in report.to_html()
    ), "Profile report should be generated."
