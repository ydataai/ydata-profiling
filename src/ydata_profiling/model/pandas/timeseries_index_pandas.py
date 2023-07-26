"""Compute statistical description of datasets."""
import pandas as pd
import numpy as np

from typing import Any

from ydata_profiling.config import Settings
from ydata_profiling.model.timeseries_index import get_time_index_description


@get_time_index_description.register
def pandas_get_time_index_description(
    df: pd.DataFrame,
    table_stats: dict,
) -> dict:
    n_series = table_stats["types"].get("TimeSeries", 0)
    length = table_stats["n"]
    start = df.index.min()
    end = df.index.max()
    if isinstance(df.index, pd.DatetimeIndex):
        freq = df.index.inferred_freq
        delta = abs(np.diff(df.index)).mean()
        delta = delta.astype(f"timedelta64[{df.index.inferred_freq}]")
        period = delta.astype(float)
    else:
        freq = None
        period = abs(np.diff(df.index)).mean()
    return {
        "n_series": n_series,
        "length": length,
        "start": start,
        "end": end,
        "frequency": freq,
        "period": period,
    }