"""Main module of pandas-profiling.

.. include:: ../../README.md
"""

from warnings import warn

from pandas_profiling.compare_reports import compare
from pandas_profiling.controller import pandas_decorator
from pandas_profiling.profile_report import ProfileReport
from pandas_profiling.version import __version__

# backend
import pandas_profiling.model.pandas  # isort:skip  # noqa

warn(
    "`import pandas_profiling` is going to be deprecated by April 1st. Please use `import ydata_profiling` instead.",
    DeprecationWarning,
    stacklevel=2,
)

__all__ = [
    "pandas_decorator",
    "ProfileReport",
    "__version__",
    "compare",
]
