from typing import Tuple

import pandas as pd

from pandas_profiling.config import Settings
from pandas_profiling.model.schema import GenericColumnResult
from pandas_profiling.model.summary_algorithms import describe_generic


@describe_generic.register
def pandas_describe_generic(
    config: Settings, series: pd.Series, summary: dict
) -> Tuple[Settings, pd.Series, GenericColumnResult]:
    """Describe generic series.

    Args:
        config: report Settings object
        series: The Series to describe.
        summary: The dict containing the series description so far.

    Returns:
        A dict containing calculated series description values.
    """

    # number of observations in the Series
    length = len(series)

    result = GenericColumnResult()
    result.n = length
    result.p_missing = (
        summary["describe_counts"].n_missing / length if length > 0 else 0
    )
    result.count = length - summary["describe_counts"].n_missing
    result.memory_size = series.memory_usage(deep=config.memory_deep)

    return config, series, result
