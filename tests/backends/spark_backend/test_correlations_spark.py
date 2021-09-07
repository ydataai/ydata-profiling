import pandas as pd
import pytest

from pandas_profiling.config import Settings
from pandas_profiling.model.correlations import Kendall
from pandas_profiling.model.pandas.correlations_pandas import pandas_spearman_compute
from pandas_profiling.model.spark.correlations_spark import spark_spearman_compute


@pytest.fixture
def correlation_data_num(spark_session):
    correlation_testdata = pd.DataFrame(
        {
            "test_num_1": [1, 2, 3, 5, 7, 8, 9],
            "test_num_2": [11, 12, 13, 15, 17, 18, 4],
        }
    )

    return spark_session.createDataFrame(correlation_testdata)


@pytest.fixture
def correlation_data_cat(spark_session):
    correlation_testdata = pd.DataFrame(
        {
            "test_cat_1": ["one", "one", "one", "two", "two", "four", "four", "five"],
            "test_cat_2": ["one", "one", "two", "two", "three", "four", "four", "two"],
            "test_cat_3": ["one", "one", "two", "two", "three", "four", "four", "two"],
        }
    )

    return spark_session.createDataFrame(correlation_testdata)


def test_spearman_spark(correlation_data_num):
    cfg = Settings()

    res = spark_spearman_compute(cfg, correlation_data_num, {})
    print(res)

    res = pandas_spearman_compute(cfg, correlation_data_num.toPandas(), {})
    print(res.to_numpy())


def test_kendall_spark(correlation_data_cat):
    cfg = Settings()
    res = Kendall.compute(cfg, correlation_data_cat.toPandas(), {})
    print(res)

    with pytest.raises(NotImplementedError):
        res = Kendall.compute(cfg, correlation_data_cat, {})
        print(res)
