"""
Test for issue 85:
https://github.com/pandas-profiling/pandas-profiling/issues/85
"""
import numpy as np
import pandas as pd

from pandas_profiling import ProfileReport
from pandas_profiling.model.typeset import Boolean


def test_issue85():
    data = {
        "booleans_type": [False, True, True],
        "booleans_type_nan": [False, True, np.nan],
        "integers": [1, 0, 0],
        "integers_nan": [1, 0, np.nan],
        "str_yes_no": ["Y", "N", "Y"],
        "str_yes_no_mixed": ["Y", "n", "y"],
        "str_yes_no_nan": ["Y", "N", np.nan],
        "str_true_false": ["True", "False", "False"],
        "str_true_false_nan": ["True", "False", np.nan],
    }

    df = pd.DataFrame(data)

    report = ProfileReport(
        df,
        pool_size=1,
        title="Dataset with <em>Boolean</em> Variables",
        samples={"head": 20},
    )
    for col, variable_stats in report.get_description()["variables"].items():
        assert (
            variable_stats["type"] == Boolean
        ), f"Variable {col} should be boolean"
