"""
Test for issue 397 (actually a PR, but ok):
https://github.com/ydataai/ydata-profiling/pull/397
"""
import numpy as np
import pandas as pd

import ydata_profiling


def test_issue397():
    # Note: warnings are expected with np.inf values
    df = pd.DataFrame.from_dict(
        {
            "float-inf": pd.Series([np.inf, 3.0, 4.0, -np.inf], dtype="float"),
            "integer": pd.Series([3, 4, 5, 6], dtype="int"),
            "float": pd.Series([3.0, 4.0, np.nan, 6], dtype="float"),
            "integer-inf": pd.Series([3, np.inf, 5, 7]),
            "cat": ["Foo", "Bar", "Great", "Var"],
        }
    )

    report = ydata_profiling.ProfileReport(
        df, vars={"num": {"low_categorical_threshold": 0}}
    )
    assert report.config.vars.num.low_categorical_threshold == 0

    description = report.description_set

    assert description.table["types"] == {"Text": 1, "Numeric": 4}

    assert description.variables["float-inf"]["p_infinite"] == 0.5
    assert description.variables["float-inf"]["n_infinite"] == 2

    assert description.variables["integer-inf"]["p_infinite"] == 0.25
    assert description.variables["integer-inf"]["n_infinite"] == 1

    assert description.variables["integer"]["p_infinite"] == 0
    assert description.variables["integer"]["n_infinite"] == 0

    assert description.variables["float"]["p_infinite"] == 0
    assert description.variables["float"]["n_infinite"] == 0

    assert "p_infinite" not in description.variables["cat"]
    assert "n_infinite" not in description.variables["cat"]
