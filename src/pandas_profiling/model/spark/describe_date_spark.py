from typing import Tuple

import pandas as pd
import numpy as np
import pyspark.sql.functions as F
from pyspark.sql import DataFrame

from pandas_profiling.config import Settings
from pandas_profiling.model.schema import DateColumnResult
from pandas_profiling.model.summary_algorithms import (
    describe_date_1d,
    histogram_compute,
    histogram_spark_compute,
)


@describe_date_1d.register
def describe_date_1d_spark(
    config: Settings,
    df: DataFrame,
    summary: dict
) -> Tuple[Settings, DataFrame, DateColumnResult]:
    """Describe a date series.

    Args:
        series: The Series to describe.
        summary: The dict containing the series description so far.

    Returns:
        A dict containing calculated series description values.
    """
    column = df.columns[0]

    expr = [
        F.min(F.col(column)).alias("min"),
        F.max(F.col(column)).alias("max")
    ]

    stats = df.agg(*expr).first().asDict()

    result = DateColumnResult()
    result.min = pd.Timestamp(stats["min"])
    result.max = pd.Timestamp(stats["max"])
    result.range = result.max - result.min

    chi_squared_threshold = config.vars.num.chi_squared_threshold

    if chi_squared_threshold > 0.0:
        result.chi_squared = None  # TODO

    sample = config.plot.histogram.sample

    if sample:
        value_counts = summary["value_counts_without_nan"]

        # cast date to timestamp, it could be improve
        values = pd.to_datetime(value_counts.index.values, infer_datetime_format=True).astype(np.int64) // 10 ** 9

        result.histogram = histogram_compute(
            config,
            values,
            summary["n_distinct"],
            weights=value_counts.values,
        )


    else:
        n_unique = summary["describe_counts"].value_counts.where("count == 1").count()
        value_counts, bins = histogram_spark_compute(
            config,
            df,
            stats['min'],
            stats['max'],
            n_unique,
        )

        # cast date to timestamp, it could be improve
        values = pd.to_datetime(value_counts.index.values, infer_datetime_format=True).astype(np.int64) // 10 ** 9

        result.histogram = np.histogram(values,
                                        bins=bins,
                                        weights=value_counts.values)

    return config, df, result
