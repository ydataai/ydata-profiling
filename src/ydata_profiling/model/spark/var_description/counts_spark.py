"""
    Pyspark counts
"""
from typing import Tuple

import pandas as pd
from pyspark.sql import DataFrame
from pyspark.sql import functions as F

from ydata_profiling.config import Settings
from ydata_profiling.model.var_description.counts import VarCounts


def get_counts_spark(config: Settings, series: DataFrame) -> VarCounts:
    """Get a VarCounts object for a spark series.
    Args:
        config: Profiling settings.
        series: Spark DataFrame column for which we want to calculate the values.
        summary: Dictionary to store the summary results.
    """
    length = series.count()

    # Count occurrences of each value
    value_counts = series.groupBy(series.columns).count()

    # Sort by count descending, persist the result
    value_counts = value_counts.sort("count", ascending=False).persist()

    # Sort by column value ascending (for frequency tables)
    value_counts_index_sorted = value_counts.sort(series.columns[0], ascending=True)

    # Count missing values
    n_missing = value_counts.where(value_counts[series.columns[0]].isNull()).first()
    n_missing = n_missing["count"] if n_missing else 0

    # Convert top 200 values to Pandas for frequency table display
    top_200_sorted = (
        value_counts_index_sorted.limit(200)
        .toPandas()
        .set_index(series.columns[0], drop=True)
        .squeeze(axis="columns")
    )

    value_counts_without_nan = (
        value_counts.dropna()
        .limit(200)
        .toPandas()
        .set_index(series.columns[0], drop=True)
        .squeeze(axis="columns")
    )

    # @chanedwin
    memory_size = 0

    return VarCounts(
        hashable=False,
        value_counts_without_nan=value_counts_without_nan,
        value_counts_index_sorted=value_counts_index_sorted,
        ordering=False,
        n_missing=n_missing,
        n=length,
        p_missing=n_missing / length,
        count=length - n_missing,
        memory_size=memory_size,
        value_counts=value_counts.persist(),
    )
