import pandas as pd
import pytest
from pyspark.sql.types import IntegerType, StringType, StructField, StructType

from pandas_profiling.config import Settings
from pandas_profiling.model.spark.persist import GlobalPersistHandler
from pandas_profiling.model.spark.sample_spark import spark_get_sample


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


def test_spark_persist(df):
    GlobalPersistHandler.persist("df", df)

    assert GlobalPersistHandler.persisted_spark_objects["df"] == df

    GlobalPersistHandler.persist("df2", df)
    GlobalPersistHandler.persist("df3", df)

    GlobalPersistHandler.unpersist("df3")

    assert len(GlobalPersistHandler.persisted_spark_objects) == 2

    GlobalPersistHandler.unpersist_all()

    assert len(GlobalPersistHandler.persisted_spark_objects) == 0
