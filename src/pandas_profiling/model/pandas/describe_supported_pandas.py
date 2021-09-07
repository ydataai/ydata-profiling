from typing import Tuple

import pandas as pd

from pandas_profiling.config import Settings
from pandas_profiling.model.schema import SupportedColumnResult
from pandas_profiling.model.summary_algorithms import (
    describe_supported,
    series_hashable,
)


@describe_supported.register
@series_hashable
def pandas_describe_supported(
    config: Settings, series: pd.Series, series_description: dict
) -> Tuple[Settings, pd.Series, SupportedColumnResult]:
    """Describe a supported series.

    Args:
        config: report Settings object
        series: The Series to describe.
        series_description: The dict containing the series description so far.

    Returns:
        A dict containing calculated series description values.
    """

    result = SupportedColumnResult()

    # number of non-NaN observations in the Series
    count = series_description["describe_generic"].count

    value_counts = series_description["describe_counts"].value_counts

    # task
    distinct_count = len(value_counts)

    # task
    unique_count = value_counts.where(value_counts == 1).count()

    result.n_distinct = distinct_count
    result.n_unique = unique_count
    # FIXME: to fmt
    result.p_distinct = distinct_count / count if count > 0 else 0
    result.is_unique = unique_count == count and count > 0
    result.p_unique = unique_count / count if count > 0 else 0

    return config, series, result
