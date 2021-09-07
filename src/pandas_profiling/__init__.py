"""Main module of pandas-profiling.

.. include:: ../../README.md
"""

import matplotlib

from pandas_profiling.controller import pandas_decorator
from pandas_profiling.profile_report import ProfileReport
from pandas_profiling.version import __version__

matplotlib.use("svg")

# backend
import pandas_profiling.model.pandas  # isort:skip  # noqa
import pandas_profiling.model.spark  # isort:skip  # noqa


__all__ = [
    "pandas_decorator",
    "ProfileReport",
    "__version__",
]
