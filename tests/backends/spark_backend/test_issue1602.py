"""
Test for issue 1602:
https://github.com/ydataai/ydata-profiling/issues/1602
"""

from pyspark.sql import types as T

from ydata_profiling import ProfileReport


def test_spark_handles_decimal_type(test_output_dir, spark_session):
    from decimal import Decimal

    spark = spark_session

    schema = T.StructType(
        [
            T.StructField("number", T.StringType(), True),
            T.StructField("decimal", T.DecimalType(10, 2), True),
        ]
    )

    data = [(f"test_{num + 1}", Decimal(num + 1)) for num in range(205)]

    data.extend([("test_1", Decimal("1.05")) for _ in range(205)])

    test_df = spark.createDataFrame(data, schema=schema)

    profile = ProfileReport(test_df, title="decimal_handling", explorative=True)
    output_file = test_output_dir / "decimal_handling.html"
    profile.to_file(output_file)

    assert output_file.exists()
