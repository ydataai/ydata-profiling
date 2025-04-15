import pandas as pd
import pytest
from pyspark.sql.types import IntegerType, StringType, StructField, StructType

from ydata_profiling.config import Settings
from ydata_profiling.model.spark.sample_spark import get_sample_spark


# FIXME: Move to data
@pytest.fixture()
def df(spark_session):
    data_pandas = pd.DataFrame(
        {
            "make": ["Jaguar", "MG", "MINI", "Rover", "Lotus"] * 50,
            "registration": ["AB98ABCD", "BC99BCDF", "CD00CDE", "DE01DEF", "EF02EFG"]
            * 50,
            "year": [1998, 1999, 2000, 2001, 2002] * 50,
        }
    )
    # Turn the data into a Spark DataFrame, self.spark comes from our PySparkTest base class
    data_spark = spark_session.createDataFrame(data_pandas)
    return data_spark


@pytest.fixture()
def df_empty(spark_session):
    data_pandas = pd.DataFrame({"make": [], "registration": [], "year": []})
    # Turn the data into a Spark DataFrame, self.spark comes from our PySparkTest base class
    schema = StructType(
        {
            StructField("make", StringType(), True),
            StructField("registration", StringType(), True),
            StructField("year", IntegerType(), True),
        }
    )
    data_spark = spark_session.createDataFrame(data_pandas, schema=schema)
    return data_spark


def test_spark_get_sample(df):
    config = Settings()
    config.samples.head = 17
    config.samples.random = 0
    config.samples.tail = 0

    res = get_sample_spark(config, df)
    assert len(res) == 1
    assert res[0].id == "head"
    assert len(res[0].data) == 17

    config = Settings()
    config.samples.head = 0
    config.samples.random = 0
    config.samples.tail = 0

    res = get_sample_spark(config, df)
    assert len(res) == 0


def test_spark_sample_empty(df_empty):
    config = Settings()
    config.samples.head = 5
    config.samples.random = 0
    config.samples.tail = 0

    res = get_sample_spark(config, df_empty)
    assert len(res) == 0
