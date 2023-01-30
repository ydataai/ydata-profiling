"""Test for the duplicates functionality"""
import numpy as np
import pandas as pd
import pytest

from ydata_profiling.model.duplicates import get_duplicates


@pytest.fixture(scope="module")
def test_data():
    np.random.seed(5)
    df = pd.DataFrame(
        np.random.randint(1, 100, (100, 5)),
        columns=["a", "b", "c", "duplicates", "count"],
    )
    df = pd.concat([df, df], axis=0)
    return df


def test_issue725(config, test_data):
    metrics, duplicates = get_duplicates(config, test_data, list(test_data.columns))
    assert metrics["n_duplicates"] == 100
    assert metrics["p_duplicates"] == 0.5
    assert set(duplicates.columns) == set(test_data.columns).union({"# duplicates"})


def test_issue725_existing(config, test_data):
    test_data = test_data.rename(columns={"count": "# duplicates"})
    with pytest.raises(ValueError):
        _, _ = get_duplicates(config, test_data, list(test_data.columns))
