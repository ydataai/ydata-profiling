from typing import Tuple

from pyspark.sql import DataFrame

from pandas_profiling.config import Settings

from pandas_profiling.model.summary_algorithms import describe_date_1d


@describe_date_1d.register
def describe_date_1d_spark(
    config: Settings, df: DataFrame, summary: dict
) -> Tuple[Settings, DataFrame, dict]:
    """Describe a date series.

    Args:
        series: The Series to describe.
        summary: The dict containing the series description so far.

    Returns:
        A dict containing calculated series description values.
    """

    return config, df, summary
