import warnings
from typing import Optional

import pandas as pd

from pandas_profiling.config import Settings
from pandas_profiling.model.correlations import PhiK


@PhiK.compute.register(Settings, pd.DataFrame, dict)
def pandas_phi_k_compute(
    config: Settings, df: pd.DataFrame, summary: dict
) -> Optional[pd.DataFrame]:
    intcols = {
        key
        for key, value in summary.items()
        # DateTime currently excluded
        # In some use cases, it makes sense to convert it to interval
        # See https://github.com/KaveIO/PhiK/issues/7
        if value["type"] == "Numeric" and 1 < value["n_distinct"]
    }

    selcols = {
        key
        for key, value in summary.items()
        if value["type"] != "Unsupported"
        and 1 < value["n_distinct"] <= config.categorical_maximum_correlation_distinct
    }
    selcols = selcols.union(intcols)

    if len(selcols) <= 1:
        return None

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        from phik import phik_matrix

        correlation = phik_matrix(df[selcols], interval_cols=list(intcols))

    return correlation
