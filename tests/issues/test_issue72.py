"""
Test for issue 72:
https://github.com/ydataai/ydata-profiling/issues/72
"""
import numpy as np
import pandas as pd

import ydata_profiling


def test_issue72_higher():
    # Showcase (and test) different ways of interfacing with config/profiling report
    df = pd.DataFrame({"A": [1, 2, 3, 3]})
    df["B"] = df["A"].apply(str)
    report = ydata_profiling.ProfileReport(df, correlations=None)
    report.config.vars.num.low_categorical_threshold = 2
    # 3 > 2, so numerical
    assert report.get_description().variables["A"]["type"] == "Numeric"
    # Strings are always categorical
    assert report.get_description().variables["B"]["type"] == "Numeric"


def test_issue72_equal():
    df = pd.DataFrame({"A": [1, 2, 3, 3]})
    df["B"] = df["A"].apply(str)
    report = ydata_profiling.ProfileReport(
        df,
        vars={"num": {"low_categorical_threshold": 3}},
        correlations=None,
    )

    # 3 == 3, so categorical
    assert report.get_description().variables["A"]["type"] == "Categorical"
    # Strings are always categorical
    assert report.get_description().variables["B"]["type"] == "Text"


def test_issue72_lower():
    df = pd.DataFrame({"A": [1, 2, 3, 3, np.nan]})
    df["B"] = df["A"].apply(str)
    report = df.profile_report(correlations=None)
    report.config.vars.num.low_categorical_threshold = 10

    # 3 < 10, so categorical
    assert report.get_description().variables["A"]["type"] == "Categorical"
    # Strings are always categorical
    assert report.get_description().variables["B"]["type"] == "Text"
