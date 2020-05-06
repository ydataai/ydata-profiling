"""Main module of pandas-profiling.

.. include:: ../../README.md
"""

from pandas_profiling.config import Config, config
from pandas_profiling.controller import pandas_decorator
from pandas_profiling.profile_report import ProfileReport
from pandas_profiling.version import __version__

clear_config = ProfileReport.clear_config
