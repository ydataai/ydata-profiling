"""Compute statistical description of datasets."""
import numpy as np
import pandas as pd
from pandas.api.types import is_numeric_dtype

from ydata_profiling.config import Settings
from ydata_profiling.model.timeseries_index import get_time_index_description


@get_time_index_description.register
def pandas_get_time_index_description(
    config: Settings,
    df: pd.DataFrame,
    table_stats: dict,
) -> dict:
    if not (is_numeric_dtype(df.index) or isinstance(df.index, pd.DatetimeIndex)):
        return {}

    n_series = table_stats["types"].get("TimeSeries", 0)
    length = table_stats["n"]
    start = df.index.min()
    end = df.index.max()
    period = abs(np.diff(df.index)).mean()
    if isinstance(df.index, pd.DatetimeIndex):
        period = pd.Timedelta(period)

    return {
        "n_series": n_series,
        "length": length,
        "start": start,
        "end": end,
        "period": period,
    }
