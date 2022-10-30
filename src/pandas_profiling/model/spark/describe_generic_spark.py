from typing import Tuple

from pyspark.sql import DataFrame

from pandas_profiling.config import Settings
from pandas_profiling.model.schema import GenericColumnResult
from pandas_profiling.model.summary_algorithms import describe_generic


@describe_generic.register
def describe_generic_spark(
    config: Settings, df: DataFrame, summary: dict
) -> Tuple[Settings, DataFrame, GenericColumnResult]:
    """Describe generic series.
    Args:
        series: The Series to describe.
        summary: The dict containing the series description so far.
    Returns:
        A dict containing calculated series description values.
    """

    # number of observations in the Series
    length = df.count()

    result = GenericColumnResult()
    result.n = length
    result.p_missing = summary["describe_counts"].n_missing / length
    result.count = length - summary["describe_counts"].n_missing

    return config, df, result
