"""
Test for issue 1722:
https://github.com/ydataai/ydata-profiling/issues/1722
"""

from ydata_profiling import ProfileReport
from datetime import date, datetime
from pyspark.sql import types as T, SparkSession

def make_non_numeric_df(spark: SparkSession):
    # Intentionally not including any numeric types
    schema = T.StructType(
        [
            T.StructField("id", T.StringType(), False),
            T.StructField("d", T.DateType(), False),
            T.StructField("ts", T.TimestampType(), False),
            T.StructField("arr", T.ArrayType(T.IntegerType()), False),
            T.StructField("mp", T.MapType(T.StringType(), T.IntegerType()), False),
            T.StructField(
                "struct",
                T.StructType(
                    [
                        T.StructField("a", T.IntegerType(), False),
                        T.StructField("b", T.StringType(), False),
                    ]
                ),
                False,
            ),
        ]
    )

    data = [
        ("r1", date(2020, 1, 1), datetime(2020, 1, 1, 12, 0), [1, 2], {"x": 1, "y": 2}, (10, "aa")),
        ("r2", date(2021, 6, 15), datetime(2021, 6, 15, 8, 30), [3], {"z": 3}, (20, "bb")),
        ("r3", date(2022, 12, 31), datetime(2022, 12, 31, 23, 59), [], {}, (30, "cc")),
    ]

    return spark.createDataFrame(data, schema=schema)


def test_issue1722(test_output_dir, spark_session):
    from pyspark.sql import functions as F

    spark = spark_session

    non_numeric_df = make_non_numeric_df(spark)

    # type casting 1
    df_casted = non_numeric_df.select(
        [
            (
                F.col(field.name).cast("string").alias(field.name)
                if isinstance(field.dataType, (T.DateType, T.TimestampType))
                else F.col(field.name)
            )
            for field in non_numeric_df.schema
        ]
    )
    # type casting 2
    complex_columns = [
        field.name
        for field in non_numeric_df.schema.fields
        if isinstance(field.dataType, (T.ArrayType, T.MapType, T.StructType))
    ]
    for col_name in complex_columns:
        df_casted = df_casted.withColumn(col_name, F.to_json(F.col(col_name)))

    profile = ProfileReport(df_casted, title="non_numeric_1722", explorative=True)
    output_file = test_output_dir / "non_numeric_1722.html"
    profile.to_file(output_file)

    assert output_file.exists()
