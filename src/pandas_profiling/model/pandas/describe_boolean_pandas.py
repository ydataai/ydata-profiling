from typing import Tuple

import pandas as pd

from pandas_profiling.config import Settings
from pandas_profiling.model.schema import BooleanColumnResult
from pandas_profiling.model.summary_algorithms import (
    describe_boolean_1d,
    series_hashable,
)


@describe_boolean_1d.register
@series_hashable
def pandas_describe_boolean_1d(
    config: Settings, series: pd.Series, summary: dict
) -> Tuple[Settings, pd.Series, BooleanColumnResult]:
    """Describe a boolean series.

    Args:
        config: report Settings object
        series: The Series to describe.
        summary: The dict containing the series description so far.

    Returns:
        A dict containing calculated series description values.
    """

    result = BooleanColumnResult()

    value_counts = summary["describe_counts"].value_counts
    result.top = value_counts.index[0]
    result.freq = value_counts.iloc[0]

    return config, series, result
