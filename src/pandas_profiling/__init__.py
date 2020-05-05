"""Main module of pandas-profiling.

.. include:: ../../README.md
"""

from pandas_profiling.config import config
from pandas_profiling.controller import pandas_decorator
from pandas_profiling.model.base import Variable
from pandas_profiling.model.describe import describe as describe_df
from pandas_profiling.model.messages import MessageType
from pandas_profiling.profile_report import ProfileReport
from pandas_profiling.report import get_report_structure
from pandas_profiling.utils.dataframe import rename_index
from pandas_profiling.utils.paths import get_config_default, get_config_minimal
from pandas_profiling.version import __version__
