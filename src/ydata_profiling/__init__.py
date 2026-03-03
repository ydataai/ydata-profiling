"""Main module of ydata-profiling.

.. include:: ../../README.md
"""
# ignore numba warnings
import warnings  # isort:skip # noqa

import importlib.util  # isort:skip # noqa
from warnings import warn

from ydata_profiling.compare_reports import compare  # isort:skip # noqa
from ydata_profiling.controller import pandas_decorator  # isort:skip # noqa
from ydata_profiling.profile_report import ProfileReport  # isort:skip # noqa
from ydata_profiling.version import __version__  # isort:skip # noqa

# backend
import ydata_profiling.model.pandas  # isort:skip  # noqa

spec = importlib.util.find_spec("pyspark")
if spec is not None:
    import ydata_profiling.model.spark  # isort:skip  # noqa

spec_numba = importlib.util.find_spec("numba")
if spec_numba is not None:
    from numba.core.errors import NumbaDeprecationWarning  # isort:skip # noqa

    warnings.simplefilter("ignore", category=NumbaDeprecationWarning)

warn(
    """
    `import ydata_profiling` is deprecated and will not receive more updates. 
    Please install fg-data-profiling via `pip install fg-data-profiling` and use `import data_profiling` instead.
    """,
    DeprecationWarning,
    stacklevel=2,
)

__all__ = [
    "pandas_decorator",
    "ProfileReport",
    "__version__",
    "compare",
]
