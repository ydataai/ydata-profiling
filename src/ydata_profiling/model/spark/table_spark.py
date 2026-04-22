from pyspark.sql import DataFrame

from ydata_profiling.config import Settings
from ydata_profiling.model.table import compute_common_table_stats, get_table_stats


@get_table_stats.register
def get_table_stats_spark(
    config: Settings, df: DataFrame, variable_stats: dict
) -> dict:
    """General statistics for the DataFrame.

    Args:
        config: report Settings object
        df: The DataFrame to describe.
        variable_stats: Previously calculated statistic on the DataFrame.

    Returns:
        A dictionary that contains the table statistics.
    """
    n = df.count()
    n_var = len(df.columns)

    result = {"n": n, "n_var": n_var}
    result.update(compute_common_table_stats(n, n_var, variable_stats))

    return result
