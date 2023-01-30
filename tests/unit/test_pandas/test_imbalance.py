import pandas as pd

from ydata_profiling.model.pandas.imbalance_pandas import column_imbalance_score


def test_column_imbalance_score_many_classes():
    value_counts = pd.Series([10, 20, 60, 10])
    assert column_imbalance_score(value_counts, len(value_counts)).round(2) == 0.21


def test_column_imbalance_score_uniform_distribution():
    value_counts = pd.Series([10, 10, 10, 10, 10])
    assert column_imbalance_score(value_counts, len(value_counts)).round(2) == 0


def test_column_imbalance_score_one_class():
    value_counts = [30]
    assert column_imbalance_score(value_counts, len(value_counts)) == 0
