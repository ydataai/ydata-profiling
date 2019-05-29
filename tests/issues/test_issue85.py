import pandas as pd
import numpy as np

import pandas_profiling


# https://github.com/pandas-profiling/pandas-profiling/issues/85
from pandas_profiling.model.base import Variable


def test_issue85():
    data = {
        "booleans_type": [False, True, True],
        "booleans_type_nan": [False, True, np.nan],
        "integers": [1, 0, 0],
        "integers_nan": [1, 0, np.nan],
        "str_yes_no": ["Y", "N", "Y"],
        "str_yes_no_mixed": ["Y", "n", "y"],
        "str_yes_no_nana": ["Y", "N", np.nan],
        "str_true_false": ["True", "False", "False"],
        "str_true_false_nan": ["True", "False", np.nan],
    }

    df = pd.DataFrame(data)

    report = df.profile_report(
        pool_size=1,
        title="Dataset with <em>Boolean</em> Categories",
        samples={"head": 20},
        check_correlation=False,
    )
    for col, variable_stats in report.get_description()["variables"].items():
        assert (
            variable_stats["type"] == Variable.TYPE_BOOL
        ), "Variable should be boolean"
