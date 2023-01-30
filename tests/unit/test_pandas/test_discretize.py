import pandas as pd

from ydata_profiling.model.pandas.discretize_pandas import (
    DiscretizationType,
    Discretizer,
)


def test_discretize_quantile():
    example_data = {
        "height": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
        "weight": [60.0, 70.0, 70.0, 80.0, 80.0, 80.0, 90.0, 90.0, 90.0, 90.0],
    }
    example_df = pd.DataFrame(example_data)
    expected_labels = {
        "height": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        "weight": [0, 1, 1, 3, 3, 3, 5, 5, 5, 5],
    }

    discretizer = Discretizer(method=DiscretizationType.QUANTILE, n_bins=10)
    expected_labels_df = pd.DataFrame(expected_labels)

    cut_bins = discretizer.discretize_dataframe(example_df)

    assert expected_labels_df.to_numpy().all() == cut_bins.to_numpy().all()


def test_discretize_uniform():
    example_data = {
        "height": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
        "weight": [60.0, 70.0, 70.0, 80.0, 80.0, 80.0, 90.0, 90.0, 90.0, 90.0],
    }
    example_df = pd.DataFrame(example_data)

    expected_labels = {
        "height": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        "weight": [0, 3, 3, 6, 6, 6, 9, 9, 9, 9],
    }
    expected_labels_df = pd.DataFrame(expected_labels)
    discretizer = Discretizer(method=DiscretizationType.QUANTILE, n_bins=10)

    cut_bins = discretizer.discretize_dataframe(example_df)

    assert expected_labels_df.to_numpy().all() == cut_bins.to_numpy().all()


def test_mixed_discretization():
    example_data = {
        "height": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
        "weight": [60.0, 70.0, 70.0, 80.0, 80.0, 80.0, 90.0, 90.0, 90.0, 90.0],
        "char": ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"],
    }
    example_df = pd.DataFrame(example_data)

    expected_labels = {
        "height": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        "weight": [0, 1, 1, 3, 3, 3, 5, 5, 5, 5],
        "char": ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"],
    }
    expected_labels_df = pd.DataFrame(expected_labels)
    discretizer = Discretizer(method=DiscretizationType.UNIFORM, n_bins=10)

    cut_bins = discretizer.discretize_dataframe(example_df)

    assert expected_labels_df.to_numpy().all() == cut_bins.to_numpy().all()
