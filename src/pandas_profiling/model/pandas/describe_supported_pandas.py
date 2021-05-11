from typing import Tuple

import pandas as pd

from pandas_profiling.config import Settings
from pandas_profiling.model.summary_algorithms import (
    describe_supported,
    series_hashable,
)


@describe_supported.register
@series_hashable
def pandas_describe_supported(
    config: Settings, series: pd.Series, series_description: dict
) -> Tuple[Settings, pd.Series, dict]:
    """Describe a supported series.

    Args:
        config: report Settings object
        series: The Series to describe.
        series_description: The dict containing the series description so far.

    Returns:
        A dict containing calculated series description values.
    """

    # number of non-NaN observations in the Series
    count = series_description["count"]

    value_counts = series_description["value_counts_without_nan"]
    distinct_count = len(value_counts)
    unique_count = value_counts.where(value_counts == 1).count()

    stats = {
        "n_distinct": distinct_count,
        "p_distinct": distinct_count / count if count > 0 else 0,
        "is_unique": unique_count == count and count > 0,
        "n_unique": unique_count,
        "p_unique": unique_count / count if count > 0 else 0,
    }
    stats.update(series_description)

    return config, series, stats
