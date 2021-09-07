from typing import Tuple

from pyspark.sql import DataFrame

from pandas_profiling.config import Settings
from pandas_profiling.model.schema import CountColumnResult
from pandas_profiling.model.summary_algorithms import describe_counts


@describe_counts.register
def describe_counts_spark(
    config: Settings, series: DataFrame, summary: dict
) -> Tuple[Settings, DataFrame, CountColumnResult]:
    """Counts the values in a series (with and without NaN, distinct).

    Args:
        series: Series for which we want to calculate the values.

    Returns:
        A dictionary with the count values (with and without NaN, distinct).
    """

    result = CountColumnResult()

    value_counts = series.groupBy(series.columns).count()
    value_counts = value_counts.sort("count", ascending=False)
    value_counts_index_sorted = value_counts.sort(series.columns[0], ascending=True)

    n_missing = value_counts.where(value_counts[series.columns[0]].isNull()).first()
    if n_missing is None:
        n_missing = 0
    else:
        n_missing = n_missing["count"]

    # max number of rows to visualise on histogram, most common values taken
    # FIXME: top-n parameter
    # to_pandas_limit = 100
    # limited_results = (
    #     value_counts.orderBy("count", ascending=False).limit(to_pandas_limit).toPandas()
    # )

    # limited_results = limited_results.set_index(series.columns[0], drop=True).squeeze(
    #     axis="columns"
    # )

    # FIXME: reduce to top-n and bottom-n
    value_counts_index_sorted = (
        value_counts_index_sorted.toPandas()
        .set_index(series.columns[0], drop=True)
        .squeeze(axis="columns")
    )

    result.n_missing = n_missing
    result.value_counts = value_counts.cache()
    result.values = value_counts_index_sorted

    return config, series, result
