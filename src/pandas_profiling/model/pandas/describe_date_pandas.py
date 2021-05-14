from typing import Tuple

import numpy as np
import pandas as pd

from pandas_profiling.config import Settings
from pandas_profiling.model.summary_algorithms import (
    chi_square,
    describe_date_1d,
    histogram_compute,
    series_handle_nulls,
    series_hashable,
)


@describe_date_1d.register
@series_hashable
@series_handle_nulls
def pandas_describe_date_1d(
    config: Settings, series: pd.Series, summary: dict
) -> Tuple[Settings, pd.Series, dict]:
    """Describe a date series.

    Args:
        config: report Settings object
        series: The Series to describe.
        summary: The dict containing the series description so far.

    Returns:
        A dict containing calculated series description values.
    """
    summary.update(
        {
            "min": pd.Timestamp.to_pydatetime(series.min()),
            "max": pd.Timestamp.to_pydatetime(series.max()),
        }
    )

    summary["range"] = summary["max"] - summary["min"]

    values = series.values.astype(np.int64) // 10 ** 9

    if config.vars.num.chi_squared_threshold > 0.0:
        summary["chi_squared"] = chi_square(values)

    summary.update(histogram_compute(config, values, summary["n_distinct"]))
    return config, values, summary
