from typing import Tuple

from pyspark.sql import DataFrame

from ydata_profiling.config import Settings
from ydata_profiling.model.summary_algorithms import describe_supported


@describe_supported.register
def describe_supported_spark(
    config: Settings, series: DataFrame, summary: dict
) -> Tuple[Settings, DataFrame, dict]:
    """Describe a supported series.
    Args:
        series: The Series to describe.
        series_description: The dict containing the series description so far.
    Returns:
        A dict containing calculated series description values.
    """

    # number of non-NaN observations in the Series
    count = summary["count"]
    n_distinct = summary["value_counts"].count()

    summary["n_distinct"] = n_distinct
    summary["p_distinct"] = n_distinct / count if count > 0 else 0

    n_unique = summary["value_counts"].where("count == 1").count()
    summary["is_unique"] = n_unique == count
    summary["n_unique"] = n_unique
    summary["p_unique"] = n_unique / count if count > 0 else 0

    return config, series, summary
