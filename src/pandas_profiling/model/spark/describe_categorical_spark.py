from typing import Tuple

from pyspark.sql import DataFrame

from pandas_profiling.config import Settings
from pandas_profiling.model.schema import CategoricalColumnResult
from pandas_profiling.model.summary_algorithms import describe_categorical_1d


@describe_categorical_1d.register
def describe_categorical_1d_spark(
    config: Settings, df: DataFrame, summary: dict
) -> Tuple[Settings, DataFrame, CategoricalColumnResult]:
    """Describe a categorical series.

    Args:
        series: The Series to describe.
        summary: The dict containing the series description so far.

    Returns:
        A dict containing calculated series description values.
    """

    # FIXME: cat description

    return config, df, CategoricalColumnResult()
