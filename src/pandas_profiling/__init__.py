"""Main module of pandas-profiling.

.. include:: ../../README.md
"""
import importlib.util

from pandas_profiling.compare_reports import compare
from pandas_profiling.controller import pandas_decorator
from pandas_profiling.profile_report import ProfileReport

# backend
import pandas_profiling.model.pandas  # isort:skip  # noqa

spec = importlib.util.find_spec("pyspark")
if spec is not None:
    import pandas_profiling.model.spark  # isort:skip  # noqa


__all__ = [
    "pandas_decorator",
    "ProfileReport",
    "compare",
]
