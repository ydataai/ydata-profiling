"""Main module of pandas-profiling.

.. include:: ../../README.md
"""
import importlib.util
from warnings import warn

from ydata_profiling.compare_reports import compare
from ydata_profiling.controller import pandas_decorator
from ydata_profiling.profile_report import ProfileReport
from ydata_profiling.version import __version__

# backend
import ydata_profiling.model.pandas  # isort:skip  # noqa

spec = importlib.util.find_spec("pyspark")
if spec is not None:
    import ydata_profiling.model.spark  # isort:skip  # noqa

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
