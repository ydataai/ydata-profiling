from collections import Counter

from pyspark.sql import DataFrame

from ydata_profiling.config import Settings
from ydata_profiling.model.table import get_table_stats


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

    result = {"n": n, "n_var": len(df.columns)}

    table_stats = {
        "n_cells_missing": 0,
        "n_vars_with_missing": 0,
        "n_vars_all_missing": 0,
    }

    for series_summary in variable_stats.values():
        if "n_missing" in series_summary and series_summary["n_missing"] > 0:
            table_stats["n_vars_with_missing"] += 1
            table_stats["n_cells_missing"] += series_summary["n_missing"]
            if series_summary["n_missing"] == n:
                table_stats["n_vars_all_missing"] += 1

    # without this check we'll get a div by zero error
    if result["n"] * result["n_var"] > 0:
        table_stats["p_cells_missing"] = (
            table_stats["n_cells_missing"] / (result["n"] * result["n_var"])
            if result["n"] > 0
            else 0
        )
    else:
        table_stats["p_cells_missing"] = 0

    result["p_cells_missing"] = table_stats["p_cells_missing"]
    result["n_cells_missing"] = table_stats["n_cells_missing"]
    result["n_vars_all_missing"] = table_stats["n_vars_all_missing"]
    result["n_vars_with_missing"] = table_stats["n_vars_with_missing"]

    # Variable type counts
    result["types"] = dict(Counter([v["type"] for v in variable_stats.values()]))

    return result
