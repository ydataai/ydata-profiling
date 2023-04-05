"""
Test for issue 437:
https://github.com/ydataai/ydata-profiling/issues/437
"""
import numpy as np
import pandas as pd

from ydata_profiling import ProfileReport


def test_issue437():
    try:
        # pd.NA does not exist in some pandas versions
        _ = pd.NA
    except:  # noqa: E722
        pass
    else:
        tmp_list = [
            0.15416284237967237,
            0.7400496965154048,
            0.26331501518513467,
            0.5337393933802977,
            0.014574962485419674,
            0.918747008099885,
            0.9007148541170122,
            0.03342142762634459,
            0.9569493362751168,
            0.13720932135607644,
        ]
        # If exist, we should handle it properly
        df = pd.DataFrame(
            {
                "a": tmp_list + [np.inf, -np.inf],
                "b": tmp_list + [None, np.nan],
                "c": tmp_list + [0, pd.NA],
            }
        )

        report = ProfileReport(df)
        description_set = report.description_set

        assert description_set.variables["a"]["type"] == "Numeric"
        assert description_set.variables["b"]["type"] == "Numeric"
        assert description_set.variables["c"]["type"] == "Numeric"
