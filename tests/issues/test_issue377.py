"""
Test for issue 377:
https://github.com/pandas-profiling/pandas-profiling/issues/377
"""
import sys

import pandas as pd
import pytest

import pandas_profiling
from pandas_profiling.utils.cache import cache_file


@pytest.mark.skipif(sys.version_info < (3, 6), reason="requires python3.6 or higher")
def test_issue377():
    file_name = cache_file(
        "bank-full.csv",
        "https://storage.googleapis.com/erwinh-public-data/bankingdata/bank-full.csv",
    )

    # Download the UCI Bank Marketing Dataset
    df = pd.read_csv(file_name, sep=";")

    original_order = tuple(df.columns.values)

    profile = pandas_profiling.ProfileReport(
        df, sort="None", pool_size=1, progress_bar=False
    )
    new_order = tuple(profile.get_description()["variables"].keys())
    assert original_order == new_order
