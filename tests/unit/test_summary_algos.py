import numpy as np
import pandas as pd
import pytest

from pandas_profiling.model.dataframe_wrappers import SparkSeries
from pandas_profiling.model.summary_algorithms import (
    describe_boolean_1d,
    describe_boolean_spark_1d,
    describe_counts,
)


def test_count_summary_sorted():
    s = pd.Series([1] + [2] * 1000)
    sn, r = describe_counts(s, {})
    assert r["value_counts_without_nan"].index[0] == 2
    assert r["value_counts_without_nan"].index[1] == 1


def test_count_summary_nat():
    s = pd.to_datetime(pd.Series([1, 2] + [np.nan, pd.NaT]))
    sn, r = describe_counts(s, {})
    assert len(r["value_counts_without_nan"].index) == 2


def test_count_summary_category():
    s = pd.Categorical(
        ["Poor", "Neutral"] + [np.nan] * 100,
        categories=["Poor", "Neutral", "Excellent"],
    )
    sn, r = describe_counts(s, {})
    assert len(r["value_counts_without_nan"].index) == 2


def test_boolean_count():
    _, results = describe_boolean_1d(
        pd.Series([{"Hello": True}, {"Hello": False}, {"Hello": True}]),
        {"hashable": True, "value_counts_without_nan": pd.Series({True: 2, False: 1})},
    )

    assert results["top"]
    assert results["freq"] == 2


@pytest.mark.sparktest
def test_boolean_count_spark(spark_session):
    sdf = spark_session.createDataFrame(
        pd.DataFrame([{"Hello": True}, {"Hello": False}, {"Hello": True}])
    )
    _, results = describe_boolean_spark_1d(
        SparkSeries(sdf), {"value_counts_without_nan": pd.Series({True: 2, False: 1})}
    )
    assert results["top"]
    assert results["freq"] == 2
