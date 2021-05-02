from typing import Tuple

import numpy as np

from pandas_profiling.config import config
from pandas_profiling.model.dataframe_wrappers import SparkDataFrame
from pandas_profiling.model.series_wrappers import SparkSeries
from pandas_profiling.model.summary_helpers import (
    histogram_compute,
    length_summary,
    unicode_summary,
    word_summary,
)


def numeric_stats_spark(df: SparkDataFrame, summary):
    import pyspark.sql.functions as F

    column_names = df.columns
    from pyspark.sql import SparkSession

    spark = SparkSession.builder.getOrCreate()

    row = [(1,)]
    final_dataframe = spark.createDataFrame(row, ["join_col"])
    for column in column_names:
        final_dataframe = final_dataframe.join(
            summary[column]["series"].series.select(
                F.mean(column).alias(f"{column}_mean"),
                F.stddev(column).alias(f"{column}_std"),
                F.variance(column).alias(f"{column}_variance"),
                F.min(column).alias(f"{column}_min"),
                F.max(column).alias(f"{column}_max"),
                F.kurtosis(column).alias(f"{column}_kurtosis"),
                F.skewness(column).alias(f"{column}_skewness"),
                F.sum(column).alias(f"{column}_sum"),
                F.lit(1).alias("join_col"),
            ),
            on="join_col",
        )

    pandas_df = final_dataframe.toPandas().T

    full_results = {}
    for column in column_names:
        results = {
            "mean": pandas_df.loc[f"{column}_mean"][0],
            "std": pandas_df.loc[f"{column}_std"][0],
            "variance": pandas_df.loc[f"{column}_variance"][0],
            "min": pandas_df.loc[f"{column}_min"][0],
            "max": pandas_df.loc[f"{column}_max"][0],
            # Unbiased kurtosis obtained using Fisher's definition (kurtosis of normal == 0.0). Normalized by N-1.
            "kurtosis": pandas_df.loc[f"{column}_kurtosis"][0],
            # Unbiased skew normalized by N-1
            "skewness": pandas_df.loc[f"{column}_skewness"][0],
            "sum": pandas_df.loc[f"{column}_sum"][0],
        }
        full_results[column] = results

    return full_results


def describe_counts_spark(
    df: SparkDataFrame, summary: dict
) -> Tuple[SparkDataFrame, dict]:
    """Counts the values in a series (with and without NaN, distinct).

    Args:
        series: Series for which we want to calculate the values.

    Returns:
        A dictionary with the count values (with and without NaN, distinct).
    """
    for column in df.columns:

        # we need to compute value counts for each column, which means this cannot be batched
        series = SparkSeries(
            df.get_spark_df().select(column),
            sample=df.sample[column],
            persist=df.persist_bool,
        )
        spark_value_counts = series.value_counts()

        # max number of rows to visualise on histogram, most common values taken
        to_pandas_limit = config["spark"]["to_pandas_limit"].get(int)
        limited_results = (
            spark_value_counts.orderBy("count", ascending=False)
            .limit(to_pandas_limit)
            .toPandas()
        )

        limited_results = (
            limited_results.sort_values("count", ascending=False)
            .set_index(series.name, drop=True)
            .squeeze(axis="columns")
        )
        series_summary = summary[column]
        series_summary.update(
            {
                "series": series,
                "value_counts_without_nan": limited_results,
                "value_counts_without_nan_spark": spark_value_counts,
                "n_missing": series.count_na(),
            }
        )

    return df, summary


def describe_supported_spark(
    df: SparkDataFrame, series_description: dict
) -> Tuple[SparkDataFrame, dict]:
    """Describe a supported series.
    Args:
        series: The Series to describe.
        series_description: The dict containing the series description so far.
    Returns:
        A dict containing calculated series description values.
    """

    # number of non-NaN observations in the Series
    for column in df.columns:
        series_summary = series_description[column]
        count = series_summary["count"]
        series = series_summary["series"]
        stats = {}
        if config["spark"]["compute_distinct"].get(bool):
            distinct_count = series.distinct
            stats.update(
                {"n_distinct": distinct_count, "p_distinct": distinct_count / count}
            )
        if config["spark"]["compute_unique"].get(bool):
            unique_count = series.unique
            stats.update(
                {
                    "is_unique": unique_count == count,
                    "n_unique": unique_count,
                    "p_unique": unique_count / count,
                }
            )
        series_summary.update(stats)

    return df, series_description


def describe_generic_spark(
    df: SparkDataFrame, summary: dict
) -> Tuple[SparkDataFrame, dict]:
    """Describe generic series.
    Args:
        series: The Series to describe.
        summary: The dict containing the series description so far.
    Returns:
        A dict containing calculated series description values.
    """

    # number of observations in the Series
    length = len(df)

    memory_usage = df.get_memory_usage()

    for column in df.columns:
        series_summary = summary[column]
        series_summary.update(
            {
                "n": length,
                "p_missing": series_summary["n_missing"] / length,
                "count": length - series_summary["n_missing"],
                "memory_size": memory_usage[column].sum(),
            }
        )

    return df, summary


def describe_numeric_1d_spark(
    df: SparkDataFrame, summary
) -> Tuple[SparkDataFrame, dict]:
    """Describe a boolean series.

    Args:
        series: The Series to describe.
        summary: The dict containing the series description so far.

    Returns:
        A dict containing calculated series description values.
    """

    # Config

    import pyspark.sql.functions as F

    numeric_stats = numeric_stats_spark(df, summary)

    for column in df.columns:
        series_summary = summary[column]
        series_summary.update(numeric_stats[column])

        value_counts = series_summary["value_counts_without_nan"]

        series = series_summary["series"]

        infinity_values = [np.inf, -np.inf]
        series_summary["n_infinite"] = series.series.where(
            series.series[series.name].isin(infinity_values)
        ).count()

        series_summary["n_zeros"] = series.series.where(f"{series.name} = 0").count()

        series_summary["n_negative"] = series.series.where(f"{series.name} < 0").count()
        series_summary["p_negative"] = (
            series_summary["n_negative"] / series_summary["n"]
        )

        quantiles = config["vars"]["num"]["quantiles"].get(list)
        quantile_threshold = config["spark"]["quantile_error"].get(float)

        series_summary.update(
            {
                f"{percentile:.0%}": value
                for percentile, value in zip(
                    quantiles,
                    series.series.stat.approxQuantile(
                        series.name, quantiles, quantile_threshold
                    ),
                )
            }
        )

        median = series_summary["50%"]

        mad = series.series.select(
            (F.abs(F.col(series.name).cast("int") - median)).alias("abs_dev")
        ).stat.approxQuantile("abs_dev", [0.5], quantile_threshold)[0]
        series_summary.update(
            {
                "mad": mad,
            }
        )

        series_summary["range"] = series_summary["max"] - series_summary["min"]

        series_summary["iqr"] = series_summary["75%"] - series_summary["25%"]
        series_summary["cv"] = (
            series_summary["std"] / series_summary["mean"]
            if series_summary["mean"]
            else np.NaN
        )
        series_summary["p_zeros"] = series_summary["n_zeros"] / series_summary["n"]

        series_summary["p_infinite"] = (
            series_summary["n_infinite"] / series_summary["n"]
        )

        # TODO - enable this feature
        # because spark doesn't have an indexing system, there isn't really the idea of monotonic increase/decrease
        # [feature enhancement] we could implement this if the user provides an ordinal column to use for ordering
        series_summary["monotonic"] = 0

        # this function only displays the top N (see config) values for a histogram.
        # This might be confusing if there are a lot of values of equal magnitude, but we cannot bring all the values to
        # display in pandas display
        # the alternative is to do this in spark natively, but it is not trivial
        series_summary.update(
            histogram_compute(
                value_counts.index.values,
                series_summary.get("n_distinct", 200),
                weights=value_counts.values,
            )
        )

    return df, summary


def describe_categorical_1d_spark(
    df: SparkDataFrame, summary: dict
) -> Tuple[SparkDataFrame, dict]:
    """Describe a categorical series.

    Args:
        series: The Series to describe.
        summary: The dict containing the series description so far.

    Returns:
        A dict containing calculated series description values.
    """

    for column in df.columns:
        series_summary = summary[column]
        series = series_summary["series"]

        # Only run if at least 1 non-missing value
        value_counts = series_summary["value_counts_without_nan"]

        # this function only displays the top N (see config) values for a histogram.
        # This might be confusing if there are a lot of values of equal magnitude, but we cannot bring all the values to
        # display in pandas display
        # the alternative is to do this in spark natively, but it is not trivial
        series_summary.update(
            histogram_compute(
                value_counts,
                series_summary.get("n_distinct", 200),
                name="histogram_frequencies",
            )
        )

        redact = config["vars"]["cat"]["redact"].get(bool)
        if not redact:
            series_summary.update({"first_rows": series.series.limit(5).toPandas()})

        # do not do chi_square for now, too slow
        # if chi_squared_threshold > 0.0:
        #    summary["chi_squared"] = chi_square_spark(series)

        check_length = config["vars"]["cat"]["length"].get(bool)
        if check_length:
            series_summary.update(length_summary(series))
            series_summary.update(
                histogram_compute(
                    series_summary["length"],
                    series_summary["length"].nunique(),
                    name="histogram_length",
                )
            )

        check_unicode = config["vars"]["cat"]["characters"].get(bool)
        if check_unicode:
            series_summary.update(unicode_summary(series))
            series_summary["n_characters_distinct"] = series_summary["n_characters"]
            series_summary["n_characters"] = series_summary[
                "character_counts"
            ].values.sum()

            try:
                series_summary["category_alias_counts"].index = series_summary[
                    "category_alias_counts"
                ].index.str.replace("_", " ")
            except AttributeError:
                pass

        words = config["vars"]["cat"]["words"]
        to_pandas_limit = config["spark"]["to_pandas_limit"].get(int)
        if words:
            limited_series = series.sample
            limited_series.astype(str)
            series_summary.update(word_summary(limited_series))
        # if coerce_str_to_date:
        #     summary["date_warning"] = warning_type_date(series)

    return df, summary


def describe_boolean_1d_spark(
    df: SparkDataFrame, summary: dict
) -> Tuple[SparkDataFrame, dict]:
    """Describe a boolean series.

    Args:
        series: The Series to describe.
        summary: The dict containing the series description so far.

    Returns:
        A dict containing calculated series description values.
    """

    for column in df.columns:
        series_summary = summary[column]

        value_counts = series_summary["value_counts_without_nan"]
        series_summary.update(
            {"top": value_counts.index[0], "freq": value_counts.iloc[0]}
        )

    return df, summary
