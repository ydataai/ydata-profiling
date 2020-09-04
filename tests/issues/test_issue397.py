"""
Test for issue 397 (actually a PR, but ok):
https://github.com/pandas-profiling/pandas-profiling/pull/397
"""
import numpy as np
import pandas as pd

import pandas_profiling
from pandas_profiling.model.typeset import Categorical, Numeric


def test_issue397():
    df = pd.DataFrame.from_dict(
        {
            "float-inf": pd.Series([np.inf, 3.0, 4.0, np.NINF], dtype="float"),
            "integer": pd.Series([3, 4, 5, 6], dtype="int"),
            "float": pd.Series([3.0, 4.0, np.nan, 6], dtype="float"),
            "integer-inf": pd.Series([3, np.inf, 5, 7]),
            "cat": ["Foo", "Bar", "Great", "Var"],
        }
    )

    report = pandas_profiling.ProfileReport(
        df, vars={"num": {"low_categorical_threshold": 0}}
    )

    description = report.description_set

    assert description["table"]["types"] == {Categorical: 1, Numeric: 4}

    assert description["variables"]["float-inf"]["p_infinite"] == 0.5
    assert description["variables"]["float-inf"]["n_infinite"] == 2

    assert description["variables"]["integer-inf"]["p_infinite"] == 0.25
    assert description["variables"]["integer-inf"]["n_infinite"] == 1

    assert description["variables"]["integer"]["p_infinite"] == 0
    assert description["variables"]["integer"]["n_infinite"] == 0

    assert description["variables"]["float"]["p_infinite"] == 0
    assert description["variables"]["float"]["n_infinite"] == 0

    assert "p_infinite" not in description["variables"]["cat"]
    assert "n_infinite" not in description["variables"]["cat"]
