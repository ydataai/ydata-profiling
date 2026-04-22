import pandas as pd

from ydata_profiling.config import Settings
from ydata_profiling.model.table import compute_common_table_stats, get_table_stats


@get_table_stats.register
def pandas_get_table_stats(
    config: Settings, df: pd.DataFrame, variable_stats: dict
) -> dict:
    """General statistics for the DataFrame.

    Args:
        config: report Settings object
        df: The DataFrame to describe.
        variable_stats: Previously calculated statistic on the DataFrame.

    Returns:
        A dictionary that contains the table statistics.
    """
    n = len(df) if not df.empty else 0
    n_var = len(df.columns)

    memory_size = df.memory_usage(deep=config.memory_deep).sum()
    record_size = float(memory_size) / n if n > 0 else 0

    table_stats = {
        "n": n,
        "n_var": n_var,
        "memory_size": memory_size,
        "record_size": record_size,
    }

    table_stats.update(compute_common_table_stats(n, n_var, variable_stats))

    return table_stats
