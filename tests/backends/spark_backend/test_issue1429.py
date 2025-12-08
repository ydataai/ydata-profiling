"""
Test for issue 1429:
https://github.com/ydataai/ydata-profiling/issues/1429
"""

from ydata_profiling.config import SparkSettings
from ydata_profiling.model.spark.describe_numeric_spark import numeric_stats_spark
from ydata_profiling.model.spark.describe_counts_spark import describe_counts_spark
from pyspark.sql import types as T, SparkSession, DataFrame


def create_test_df(spark: SparkSession) -> DataFrame:
    schema = T.StructType(
        [
            T.StructField("category", T.StringType(), True),
            T.StructField("double", T.DoubleType(), True),
            T.StructField("int", T.IntegerType(), True),
            T.StructField("boolean", T.BooleanType(), True),
        ]
    )

    data = [
        (f"test_{num + 1}", float(num), int(num), True) for num in range(205)
    ]

    # Adding dupes
    data.extend(
        [
            ("test_1", float(1), int(1), False) for _ in range(205)
        ]
    )

    # Adding nulls
    data.extend(
        [
            (None, None, None, None) for _ in range(100)
        ]
    )

    return spark.createDataFrame(data, schema=schema)


def test_describe_numeric_spark(spark_session):
    test_df = create_test_df(spark_session)

    numeric_stats = numeric_stats_spark(df=test_df.select("double"), summary={})

    for _, value in numeric_stats.items():
        assert value is not None


def test_describe_counts_spark(spark_session):
    test_df = create_test_df(spark_session)

    _, _, summary = describe_counts_spark(config=SparkSettings(), series=test_df.select("category"), summary={})

    assert summary["value_counts_without_nan"].loc["test_1"] == 206

    _, _, summary = describe_counts_spark(config=SparkSettings(), series=test_df.select("double"), summary={})

    assert summary["value_counts_without_nan"].loc[float(1)] == 206

    _, _, summary = describe_counts_spark(config=SparkSettings(), series=test_df.select("int"), summary={})

    assert summary["value_counts_without_nan"].loc[int(1)] == 206

    _, _, summary = describe_counts_spark(config=SparkSettings(), series=test_df.select("boolean"), summary={})

    assert summary["value_counts_without_nan"].loc[True] == 205
