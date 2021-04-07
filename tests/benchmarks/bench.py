import pandas as pd

from pandas_profiling import ProfileReport
from pandas_profiling.utils.cache import cache_file


def test_titanic_explorative(benchmark):
    file_name = cache_file(
        "titanic.parquet",
        "https://github.com/pandas-profiling/pandas-profiling-data/raw/master/data/titanic.parquet",
    )

    data = pd.read_parquet(file_name)

    def func(df):
        profile = ProfileReport(
            df, title="Titanic Dataset", explorative=True, progress_bar=False
        )
        report = profile.to_html()
        return report

    benchmark(func, data)


def test_titanic_default(benchmark):
    file_name = cache_file(
        "titanic.parquet",
        "https://github.com/pandas-profiling/pandas-profiling-data/raw/master/data/titanic.parquet",
    )

    data = pd.read_parquet(file_name)

    def func(df):
        profile = ProfileReport(df, title="Titanic Dataset", progress_bar=False)
        report = profile.to_html()
        return report

    benchmark(func, data)


def test_titanic_minimal(benchmark):
    file_name = cache_file(
        "titanic.parquet",
        "https://github.com/pandas-profiling/pandas-profiling-data/raw/master/data/titanic.parquet",
    )

    data = pd.read_parquet(file_name)

    def func(df):
        profile = ProfileReport(
            df, title="Titanic Dataset", minimal=True, progress_bar=False
        )
        report = profile.to_html()
        return report

    benchmark(func, data)


# def test_rdw_minimal(benchmark):
#     file_name = cache_file(
#         "rdw.parquet",
#         "https://github.com/pandas-profiling/pandas-profiling-data/raw/master/data/rdw.parquet",
#     )
#
#     data = pd.read_parquet(file_name)
#
#     def func(df):
#         profile = ProfileReport(
#             df, title="RDW Dataset", minimal=True, progress_bar=False
#         )
#         report = profile.to_html()
#         return report
#
#     benchmark(func, data)
