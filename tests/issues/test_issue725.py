"""
Test for issue 725:
https://github.com/pandas-profiling/pandas-profiling/issues/725
"""
import numpy as np
import pandas as pd
import pytest

from pandas_profiling.model.duplicates import get_duplicates


@pytest.fixture(scope="module")
def test_data():
    np.random.seed(5)
    df = pd.DataFrame(
        np.random.randint(1, 100, (100, 5)),
        columns=["a", "b", "c", "duplicates", "count"],
    )
    df = pd.concat([df, df], axis=0)
    return df


def test_issue725(test_data):
    duplicates = get_duplicates(test_data, list(test_data.columns))
    assert set(duplicates.columns) == set(test_data.columns).union({"# duplicates"})


def test_issue725_existing(test_data):
    test_data = test_data.rename(columns={"count": "# duplicates"})
    with pytest.raises(ValueError):
        _ = get_duplicates(test_data, list(test_data.columns))
