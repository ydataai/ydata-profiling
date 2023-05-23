from ydata_profiling.config import Settings
from ydata_profiling.model.pandas.table_pandas import pandas_get_table_stats
from ydata_profiling.model.table import get_table_stats
from ydata_profiling.utils import modin


@get_table_stats.register
def modin_get_table_stats(
    config: Settings, df: modin.DataFrame, variable_stats: dict
) -> dict:
    return pandas_get_table_stats(config, df, variable_stats)
