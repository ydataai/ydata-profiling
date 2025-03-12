"""Compute statistical description of datasets."""
from pyspark.sql import DataFrame

from ydata_profiling.config import Settings


def spark_get_time_index_description_spark(
    config: Settings,
    df: DataFrame,
    table_stats: dict,
) -> dict:
    return {}
