from typing import Tuple

import numpy as np
import pyspark.sql.functions as F
from pyspark.sql import DataFrame

from pandas_profiling.config import Settings
from pandas_profiling.model.schema import NumericColumnResult
from pandas_profiling.model.summary_algorithms import (
    describe_numeric_1d,
    histogram_compute,
    histogram_spark_compute,
)

def numeric_stats_spark(df: DataFrame) -> dict:
    column = df.columns[0]

    expr = [
        F.mean(F.col(column)).alias("mean"),
        F.stddev(F.col(column)).alias("std"),
        F.variance(F.col(column)).alias("variance"),
        F.min(F.col(column)).alias("min"),
        F.max(F.col(column)).alias("max"),
        F.kurtosis(F.col(column)).alias("kurtosis"),
        F.skewness(F.col(column)).alias("skewness"),
        F.sum(F.col(column)).alias("sum"),
    ]
    return df.agg(*expr).first().asDict()


@describe_numeric_1d.register
def describe_numeric_1d_spark(
    config: Settings, df: DataFrame, summary: dict
) -> Tuple[Settings, DataFrame, NumericColumnResult]:
    """Describe a boolean series.

    Args:
        series: The Series to describe.
        summary: The dict containing the series description so far.

    Returns:
        A dict containing calculated series description values.
    """
    column_name = df.columns[0]

    result = NumericColumnResult()

    stats = numeric_stats_spark(df)
    # summary.update(numeric_stats)
    result.min = stats["min"]
    result.max = stats["max"]
    result.mean = stats["mean"]
    result.std = stats["std"]
    result.variance = stats["variance"]
    result.skewness = stats["skewness"]
    result.kurtosis = stats["kurtosis"]
    result.sum = stats["sum"]

    value_counts = summary["describe_counts"].value_counts

    n_infinite = (
        value_counts.where(F.col(column_name).isin([np.inf, -np.inf]))
        .agg(F.sum(F.col("count")).alias("count"))
        .first()
    )
    if n_infinite is None or n_infinite["count"] is None:
        n_infinite = 0
    else:
        n_infinite = n_infinite["count"]
    result.n_infinite = n_infinite

    n_zeros = value_counts.where(f"{column_name} = 0").first()
    if n_zeros is None:
        n_zeros = 0
    else:
        n_zeros = n_zeros["count"]
    result.n_zeros = n_zeros

    n_negative = (
        value_counts.where(f"{column_name} < 0")
        .agg(F.sum(F.col("count")).alias("count"))
        .first()
    )
    if n_negative is None or n_negative["count"] is None:
        n_negative = 0
    else:
        n_negative = n_negative["count"]
    result.n_negative = n_negative

    quantiles = config.vars.num.quantiles
    quantile_threshold = 0.05

    result.quantiles = {
        f"{percentile:.0%}": value
        for percentile, value in zip(
            quantiles,
            df.stat.approxQuantile(
                f"{column_name}",
                quantiles,
                quantile_threshold,
            ),
        )
    }

    median = result.quantiles["50%"]

    result.mad = df.select(
        (F.abs(F.col(f"{column_name}").cast("int") - median)).alias("abs_dev")
    ).stat.approxQuantile("abs_dev", [0.5], quantile_threshold)[0]

    # FIXME: move to fmt
    result.p_negative = result.n_negative / summary["describe_generic"].n
    result.range = result.max - result.min
    result.iqr = result.quantiles["75%"] - result.quantiles["25%"]
    result.cv = result.std / result.mean if result.mean else np.NaN
    result.p_zeros = result.n_zeros / summary["describe_generic"].n
    result.p_infinite = result.n_infinite / summary["describe_generic"].n

    # TODO - enable this feature
    # because spark doesn't have an indexing system, there isn't really the idea of monotonic increase/decrease
    # [feature enhancement] we could implement this if the user provides an ordinal column to use for ordering
    # ... https://stackoverflow.com/questions/60221841/how-to-detect-monotonic-decrease-in-pyspark
    # summary["monotonic"] =

    # this function only displays the top N (see config) values for a histogram.

    sample = config.plot.histogram.sample

    if sample:
        result.histogram = histogram_compute(
            config,
            value_counts.index.values,
            summary["n_distinct"],
            weights=value_counts.values,
        )

    else:
        n_unique = summary["describe_counts"].value_counts.where("count == 1").count()
        value_counts, bins = histogram_spark_compute(config,
                                                     df=df,
                                                     minim= result.min,
                                                     maxim=result.max,
                                                     n_unique=n_unique,
                                                     )

        result.histogram = np.histogram(value_counts.index.values,
                                        bins=bins,
                                        weights=value_counts.values)

    return config, df, result
