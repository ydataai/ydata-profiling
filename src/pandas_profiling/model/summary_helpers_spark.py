from collections import Counter

from pandas_profiling.config import config
from pandas_profiling.model.series_wrappers import SparkSeries


def named_aggregate_summary_spark(series: SparkSeries, key: str):
    import pyspark.sql.functions as F

    lengths = series.series.select(F.length(series.name).alias("length"))

    # do not count length of nans
    numeric_results_df = (
        lengths.select(
            F.mean("length").alias("mean"),
            F.min("length").alias("min"),
            F.max("length").alias("max"),
        )
        .toPandas()
        .T
    )

    quantile_error = config["spark"]["quantile_error"].get(float)
    median = lengths.stat.approxQuantile("length", [0.5], quantile_error)[0]
    summary = {
        f"max_{key}": numeric_results_df.loc["max"][0],
        f"mean_{key}": numeric_results_df.loc["mean"][0],
        f"median_{key}": median,
        f"min_{key}": numeric_results_df.loc["min"][0],
    }

    return summary


def length_summary_spark(series: SparkSeries, summary: dict = {}) -> dict:
    # imported here to avoid circular imports
    from pandas_profiling.model.summary_helpers import named_aggregate_summary

    length = series.sample.dropna().str.len()

    summary.update({"length": length})
    summary.update(named_aggregate_summary(series, "length"))

    return summary


def get_character_counts_spark(series: SparkSeries) -> Counter:
    """Function to return the character counts

    Args:
        series: the Series to process

    Returns:
        A dict with character counts
    """
    import pyspark.sql.functions as F

    # this function is optimised to split all characters and explode the characters and then groupby the characters
    # because the number of characters is limited, the return dataset is small -> can return everything to pandas
    df = (
        series.series.select(F.explode(F.split(F.col(series.name), "")))
        .groupby("col")
        .count()
        .toPandas()
    )

    # standardise return as Counter object
    my_dict = Counter(
        {
            x[0]: x[1]
            for x in filter(lambda x: x[0], zip(df["col"].values, df["count"].values))
        }
    )

    return my_dict
