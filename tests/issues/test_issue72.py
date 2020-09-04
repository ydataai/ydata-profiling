"""
Test for issue 72:
https://github.com/pandas-profiling/pandas-profiling/issues/72
"""
import numpy as np
import pandas as pd

import pandas_profiling
from pandas_profiling.config import config
from pandas_profiling.model.typeset import Numeric, Categorical


def test_issue72_higher():
    # Showcase (and test) different ways of interfacing with config/profiling report
    config["vars"]["num"]["low_categorical_threshold"].set(2)
    config["correlations"]["recoded"]["calculate"].set(False)

    df = pd.DataFrame({"A": [1, 2, 3, 3]})
    df["B"] = df["A"].apply(str)
    report = pandas_profiling.ProfileReport(df)

    # 3 > 2, so numerical
    assert report.get_description()["variables"]["A"]["type"] == Numeric
    # Strings are always categorical
    assert report.get_description()["variables"]["B"]["type"] == Categorical


def test_issue72_equal():
    df = pd.DataFrame({"A": [1, 2, 3, 3]})
    df["B"] = df["A"].apply(str)
    report = pandas_profiling.ProfileReport(
        df,
        vars={"num": {"low_categorical_threshold": 3}},
        correlations={"recoded": {"calculate": False}},
    )

    # 3 == 3, so numerical
    assert report.get_description()["variables"]["A"]["type"] == Numeric
    # Strings are always categorical
    assert report.get_description()["variables"]["B"]["type"] == Categorical


def test_issue72_lower():
    config["vars"]["num"]["low_categorical_threshold"].set(10)

    df = pd.DataFrame({"A": [1, 2, 3, 3, np.nan]})
    df["B"] = df["A"].apply(str)
    report = df.profile_report(correlations={"recoded": {"calculate": False}})

    # 3 < 10, so categorical
    assert report.get_description()["variables"]["A"]["type"] == Categorical
    # Strings are always categorical
    assert report.get_description()["variables"]["B"]["type"] == Categorical
