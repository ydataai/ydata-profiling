import numpy as np
import pandas as pd

from pandas_profiling.model.summary_algorithms import (
    describe_counts,
    describe_supported,
    describe_generic,
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


def test_count_summary_empty_df():
    s = pd.DataFrame({'A': []})
    sn, r = describe_counts(s, {})
    assert r['n_missing'].index == 'A'


def test_summary_supported_empty_df():
    s = pd.DataFrame({'A': []})
    s, series_description = describe_counts(s, {})
    sn, r = describe_supported(s, series_description)
    assert r['n_missing'].index == 'A'


def test_summary_generric_empty_df():
    s = pd.DataFrame({'A': []})
    s, summary = describe_counts(s, {})
    sn, r = describe_generic(s, summary)
    assert r["p_missing"] == 0

