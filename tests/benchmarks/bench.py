from functools import partial

import pandas as pd

from pandas_profiling import ProfileReport
from pandas_profiling.utils.cache import cache_file


def func(df, **kwargs):
    profile = ProfileReport(df, progress_bar=False, **kwargs)
    report = profile.to_html()
    return report


def test_titanic_explorative(benchmark):
    file_name = cache_file(
        "titanic.parquet",
        "https://github.com/pandas-profiling/pandas-profiling-data/raw/master/data/titanic.parquet",
    )

    data = pd.read_parquet(file_name)

    kwargs = {"explorative": True}
    benchmark(partial(func, **kwargs), data)


def test_titanic_default(benchmark):
    file_name = cache_file(
        "titanic.parquet",
        "https://github.com/pandas-profiling/pandas-profiling-data/raw/master/data/titanic.parquet",
    )

    data = pd.read_parquet(file_name)

    benchmark(partial(func), data)


def test_titanic_minimal(benchmark):
    file_name = cache_file(
        "titanic.parquet",
        "https://github.com/pandas-profiling/pandas-profiling-data/raw/master/data/titanic.parquet",
    )

    data = pd.read_parquet(file_name)

    kwargs = {"minimal": True}
    benchmark(partial(func, **kwargs), data)


def test_rdw_minimal(benchmark):
    file_name = cache_file(
        "rdw_sample_100k.parquet",
        "https://github.com/pandas-profiling/pandas-profiling-data/raw/master/data/rdw_sample_100k.parquet",
    )

    data = pd.read_parquet(file_name)

    kwargs = {"minimal": True}
    benchmark(partial(func, **kwargs), data)
