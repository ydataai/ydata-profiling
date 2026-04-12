from collections import Counter
from typing import Any

from multimethod import multimethod

from ydata_profiling.config import Settings


def compute_common_table_stats(
    n: int, n_var: int, variable_stats: dict
) -> dict:
    """Compute common table statistics shared by Pandas and Spark backends.

    Args:
        n: Number of rows in the DataFrame
        n_var: Number of columns (variables)
        variable_stats: Previously calculated statistic on the DataFrame series

    Returns:
        A dictionary with common table statistics: missing values counts, percentages, and type counts
    """
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

    total_cells = n * n_var
    table_stats["p_cells_missing"] = (
        table_stats["n_cells_missing"] / total_cells if total_cells > 0 else 0
    )

    table_stats["types"] = dict(Counter([v["type"] for v in variable_stats.values()]))

    return table_stats


@multimethod
def get_table_stats(config: Settings, df: Any, variable_stats: dict) -> dict:
    raise NotImplementedError()
