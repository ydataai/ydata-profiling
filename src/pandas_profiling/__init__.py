"""Main module of pandas-profiling.

.. include:: ../../README.md
"""

from pandas_profiling.controller import pandas_decorator
from pandas_profiling.profile_report import ProfileReport
from pandas_profiling.version import __version__

# backend
import pandas_profiling.model.pandas  # isort:skip  # noqa


__all__ = [
    "pandas_decorator",
    "ProfileReport",
    "__version__",
]
