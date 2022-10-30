from typing import Tuple

from pyspark.sql import DataFrame

from pandas_profiling.config import Settings
from pandas_profiling.model.schema import SupportedColumnResult
from pandas_profiling.model.summary_algorithms import describe_supported


@describe_supported.register
def describe_supported_spark(
    config: Settings, series: DataFrame, summary: dict
) -> Tuple[Settings, DataFrame, SupportedColumnResult]:
    """Describe a supported series.
    Args:
        series: The Series to describe.
        series_description: The dict containing the series description so far.
    Returns:
        A dict containing calculated series description values.
    """

    result = SupportedColumnResult()
    # number of non-NaN observations in the Series
    count = summary["describe_generic"].count
    n_distinct = summary["describe_counts"].value_counts.count()

    result.n_distinct = n_distinct
    result.p_distinct = n_distinct / count if count > 0 else 0

    n_unique = summary["describe_counts"].value_counts.where("count == 1").count()
    result.is_unique = n_unique == count
    result.n_unique = n_unique
    result.p_unique = n_unique / count

    return config, series, result
