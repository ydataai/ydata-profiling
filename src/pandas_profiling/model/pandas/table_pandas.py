from collections import Counter

import pandas as pd

from pandas_profiling.config import Settings
from pandas_profiling.model.schema import TableResult
from pandas_profiling.model.table import get_table_stats


@get_table_stats.register
def pandas_get_table_stats(
    config: Settings, df: pd.DataFrame, variable_stats: dict
) -> TableResult:
    """General statistics for the DataFrame.

    Args:
        config: report Settings object
        df: The DataFrame to describe.
        variable_stats: Previously calculated statistic on the DataFrame.

    Returns:
        A dictionary that contains the table statistics.
    """
    n = len(df)

    memory_size = df.memory_usage(deep=config.memory_deep).sum()

    result = TableResult()
    result.n = n
    result.n_var = len(df.columns)
    result.memory_size = memory_size
    result.record_size = float(memory_size) / n if n > 0 else 0

    result.n_cells_missing = 0
    result.n_vars_with_missing = 0
    result.n_vars_all_missing = 0
    for series_summary in variable_stats.values():
        if "n_missing" in series_summary and series_summary["n_missing"] > 0:
            result.n_vars_with_missing += 1
            result.n_cells_missing += series_summary["n_missing"]
            if series_summary["n_missing"] == n:
                result.n_vars_all_missing += 1

    result.p_cells_missing = (
        result.n_cells_missing / (result.n * result.n_var) if result.n > 0 else 0
    )

    # Variable type counts
    result.types = dict(Counter([v["type"] for v in variable_stats.values()]))

    return result
