from typing import Tuple

from pyspark.sql import DataFrame

from ydata_profiling.config import Settings


def describe_generic_spark(
    config: Settings, df: DataFrame, summary: dict
) -> Tuple[Settings, DataFrame, dict]:
    """Describe generic series.
    Args:
        series: The Series to describe.
        summary: The dict containing the series description so far.
    Returns:
        A dict containing calculated series description values.
    """

    # number of observations in the Series
    length = df.count()

    summary["n"] = length
    summary["p_missing"] = summary["n_missing"] / length
    summary["count"] = length - summary["n_missing"]

    # FIXME: This is not correct, but used to fulfil render expectations
    # @chanedwin
    summary["memory_size"] = 0

    return config, df, summary
