from typing import Tuple

import pandas as pd

from pandas_profiling.config import Settings
from pandas_profiling.model.pandas.imbalance_pandas import column_imbalance_score
from pandas_profiling.model.summary_algorithms import (
    describe_boolean_1d,
    series_hashable,
)


@describe_boolean_1d.register
@series_hashable
def pandas_describe_boolean_1d(
    config: Settings, series: pd.Series, summary: dict
) -> Tuple[Settings, pd.Series, dict]:
    """Describe a boolean series.

    Args:
        config: report Settings object
        series: The Series to describe.
        summary: The dict containing the series description so far.

    Returns:
        A dict containing calculated series description values.
    """

    value_counts = summary["value_counts_without_nan"]
    summary.update({"top": value_counts.index[0], "freq": value_counts.iloc[0]})

    summary["imbalance"] = column_imbalance_score(value_counts, len(value_counts))

    return config, series, summary
