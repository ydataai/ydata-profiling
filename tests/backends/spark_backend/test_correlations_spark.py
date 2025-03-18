import pandas as pd
import pytest

from ydata_profiling.config import Settings
from ydata_profiling.model.pandas.correlations_pandas import (
    pearson_compute as pandas_pearson_compute,
)
from ydata_profiling.model.pandas.correlations_pandas import (
    spearman_compute as pandas_spearman_compute,
)
from ydata_profiling.model.spark.correlations_spark import (
    pearson_compute as spark_pearson_compute,
)
from ydata_profiling.model.spark.correlations_spark import (
    spearman_compute as spark_spearman_compute,
)


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


@pytest.fixture
def correlation_var_types():
    return {"test_num_1": {"type": "Numeric"}, "test_num_2": {"type": "Numeric"}}


def test_spearman_spark(correlation_data_num, correlation_var_types):
    cfg = Settings()

    res_spark = spark_spearman_compute(
        cfg,
        correlation_data_num,
        correlation_var_types,
    )

    res_pandas = pandas_spearman_compute(cfg, correlation_data_num.toPandas(), {})

    pd.testing.assert_frame_equal(res_pandas, res_spark)


def test_pearson_spark(correlation_data_num, correlation_var_types):
    cfg = Settings()

    res_spark = spark_pearson_compute(
        cfg,
        correlation_data_num,
        correlation_var_types,
    )

    res_pandas = pandas_pearson_compute(cfg, correlation_data_num.toPandas(), {})

    pd.testing.assert_frame_equal(res_pandas, res_spark)


def test_kendall_spark(correlation_data_cat):
    from ydata_profiling.model.spark.correlations_spark import kendall_compute

    cfg = Settings()

    with pytest.raises(NotImplementedError):
        kendall_compute(config=cfg, df=correlation_data_cat, summary={})
