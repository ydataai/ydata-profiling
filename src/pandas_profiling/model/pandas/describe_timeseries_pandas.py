from typing import Tuple

import pandas as pd
from statsmodels.tsa.stattools import adfuller

from pandas_profiling.config import Settings
from pandas_profiling.model.summary_algorithms import (
    describe_numeric_1d,
    describe_timeseries_1d,
    series_handle_nulls,
    series_hashable,
)


def is_stationary(config: Settings, series: pd.Series) -> bool:
    addfuler_config = config.vars.timeseries.adfuller
    significance_threshold = addfuler_config["significance"]
    autolag = addfuler_config["autolag"]

    # make sure the data has no missing values
    adfuller_test = adfuller(series.dropna(), autolag=autolag)
    p_value = adfuller_test[1]

    return p_value >= significance_threshold


@describe_timeseries_1d.register
@series_hashable
@series_handle_nulls
def pandas_describe_timeseries_1d(
    config: Settings, series: pd.Series, summary: dict
) -> Tuple[Settings, pd.Series, dict]:
    """Describe a timeseries.

    Args:
        config: report Settings object
        series: The Series to describe.
        summary: The dict containing the series description so far.

    Returns:
        A dict containing calculated series description values.
    """
    config, series, stats = describe_numeric_1d(config, series, summary)

    stats["stationary"] = is_stationary(config, series)
    stats["series"] = series

    return config, series, stats
