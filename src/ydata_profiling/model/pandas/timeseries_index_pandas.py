"""Compute statistical description of datasets."""
import pandas as pd
import numpy as np
from ydata_profiling.config import Settings

from ydata_profiling.model.timeseries_index import get_time_index_description


@get_time_index_description.register
def pandas_get_time_index_description(
    config: Settings,
    df: pd.DataFrame,
    table_stats: dict,
    variables: dict,
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
    
    plot = create_ts_plot(config, df, variables)
    return {
        "n_series": n_series,
        "length": length,
        "start": start,
        "end": end,
        "frequency": freq,
        "period": period,
        "plot": plot,
    }

from ydata_profiling.visualisation.context import manage_matplotlib_context
from ydata_profiling.visualisation.utils import plot_360_n0sc0pe

@manage_matplotlib_context()
def create_ts_plot(config, df, variables):
    import matplotlib.pyplot as plt
    fig = plt.figure(figsize=(6, 4))
    ax = fig.add_subplot(111)
    for col, data_type in variables.items():
        if data_type == "TimeSeries":
            df[col].plot(ax=ax)
    return plot_360_n0sc0pe(config)