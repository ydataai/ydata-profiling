"""
    Pyspark counts
"""
from typing import Tuple

from ydata_profiling.config import Settings

from pyspark.sql import DataFrame, functions as F
from ydata_profiling.model.summary_algorithms import describe_counts

@describe_counts.register
def describe_counts_spark(
    config: Settings, series: DataFrame, summary: dict
) -> Tuple[Settings, DataFrame, dict]:
    """Counts the values in a series (with and without NaN, distinct).

    Args:
        config: Profiling settings.
        series: Spark DataFrame column for which we want to calculate the values.
        summary: Dictionary to store the summary results.

    Returns:
        Updated settings, input series, and summary dictionary.
    """

    # Count occurrences of each value
    value_counts = series.groupBy(series.columns[0]).count()

    # Sort by count descending, persist the result
    value_counts = value_counts.orderBy(F.desc("count")).persist()

    # Sort by column value ascending (for frequency tables)
    value_counts_index_sorted = value_counts.orderBy(F.asc(series.columns[0]))

    # Count missing values
    n_missing = value_counts.filter(F.col(series.columns[0]).isNull()).select("count").first()
    n_missing = n_missing["count"] if n_missing else 0

    # Convert top 200 values to Pandas for frequency table display
    top_200_sorted = (
        value_counts_index_sorted.limit(200)
        .toPandas()
        .set_index(series.columns[0], drop=True)
        .squeeze(axis="columns")
    )

    summary["n_missing"] = n_missing
    summary["value_counts"] = value_counts.persist()
    summary["value_counts_index_sorted"] = top_200_sorted

    column = series.columns[0]

    # Compute value counts without NaNs
    value_counts_no_nan = (
        value_counts
        .filter(F.col(column).isNotNull())  # Exclude NaNs
        .filter(~F.isnan(F.col(column)))  # Remove implicit NaNs (if numeric column)
        .groupBy(column)  # Group by unique values
        .count()  # Count occurrences
        .orderBy(F.desc("count"))  # Sort in descending order
        .limit(200)  # Limit for performance
    )

    # Convert to Pandas Series (after collecting)
    summary["value_counts_without_nan"] = (
        value_counts_no_nan.toPandas()
        .set_index(column)["count"]  # Set index to the column values
        .squeeze()  # Convert DataFrame to Pandas Series
    )

    return config, series, summary