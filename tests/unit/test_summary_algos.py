import numpy as np
import pandas as pd
import pytest

from pandas_profiling.model.summary_algorithms import (
    describe_counts,
    describe_generic,
    describe_supported,
)


def test_count_summary_sorted(config):
    s = pd.Series([1] + [2] * 1000)
    _, sn, r = describe_counts(config, s, {})
    assert r.value_counts.index[0] == 2
    assert r.value_counts.index[1] == 1


def test_count_summary_nat(config):
    s = pd.to_datetime(pd.Series([1, 2] + [np.nan, pd.NaT]))
    _, sn, r = describe_counts(config, s, {})
    assert len(r.value_counts.index) == 2


def test_count_summary_category(config):
    s = pd.Series(
        pd.Categorical(
            ["Poor", "Neutral"] + [np.nan] * 100,
            categories=["Poor", "Neutral", "Excellent"],
        )
    )
    _, sn, r = describe_counts(config, s, {})
    assert len(r.value_counts.index) == 2


@pytest.fixture(scope="class")
def empty_data() -> pd.DataFrame:
    return pd.DataFrame({"A": []})


def test_summary_supported_empty_df(config, empty_data):
    _, series, summary_count = describe_counts(config, empty_data["A"], {})
    assert summary_count.n_missing == 0

    _, series, summary_generic = describe_generic(
        config, series, {"describe_counts": summary_count}
    )
    assert summary_generic.p_missing == 0
    assert summary_generic.count == 0

    _, _, summary = describe_supported(
        config,
        series,
        {"describe_generic": summary_generic, "describe_counts": summary_count},
    )
    assert summary.n_distinct == 0
    assert summary.p_distinct == 0
    assert summary.n_unique == 0
    assert not summary.is_unique
