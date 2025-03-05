from typing import Tuple

import numpy as np
import pandas as pd

from ydata_profiling.config import Settings
from ydata_profiling.model.pandas.imbalance_pandas import column_imbalance_score
from ydata_profiling.model.summary_algorithms import describe_boolean_1d
from ydata_profiling.model.var_description.default import VarDescription


@describe_boolean_1d.register
def pandas_describe_boolean_1d(
    config: Settings, series: pd.Series, summary: VarDescription
) -> Tuple[Settings, pd.Series, VarDescription]:
    """Describe a boolean series.

    Args:
        config: report Settings object
        series: The Series to describe.
        summary: The dict containing the series description so far.

    Returns:
        A dict containing calculated series description values.
    """
    value_counts: pd.Series = summary.value_counts_without_nan
    if not value_counts.empty:
        summary.update({"top": value_counts.index[0], "freq": value_counts.iloc[0]})
        summary["imbalance"] = column_imbalance_score(value_counts, len(value_counts))
    else:
        summary.update(
            {
                "top": np.nan,
                "freq": 0,
                "imbalance": 0,
            }
        )

    return config, series, summary
