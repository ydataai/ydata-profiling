"""
Test for issue 377:
https://github.com/ydataai/ydata-profiling/issues/377
"""
import sys

import pandas as pd
import pytest
import requests

from ydata_profiling import ProfileReport
from ydata_profiling.utils.cache import cache_zipped_file


@pytest.fixture()
def df():
    try:
        file_name = cache_zipped_file(
            "bank-full.csv",
            "https://archive.ics.uci.edu/ml/machine-learning-databases/00222/bank.zip",
        )
    except (requests.exceptions.ConnectionError, FileNotFoundError):
        return

    # Download the UCI Bank Marketing Dataset
    df = pd.read_csv(file_name, sep=";")
    return df


@pytest.mark.skipif(sys.version_info < (3, 6), reason="requires python3.6 or higher")
def test_issue377(df):
    if df is None:
        pytest.skip("dataset unavailable")
        return

    original_order = tuple(df.columns.values)

    profile = ProfileReport(df, sort=None, pool_size=1, progress_bar=False)
    new_order = tuple(profile.get_description()["variables"].keys())
    assert original_order == new_order
