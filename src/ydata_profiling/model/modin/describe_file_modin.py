from typing import Tuple

from ydata_profiling.config import Settings
from ydata_profiling.model.pandas.describe_file_pandas import pandas_describe_file_1d
from ydata_profiling.model.summary_algorithms import describe_file_1d
from ydata_profiling.utils import modin


@describe_file_1d.register
def modin_describe_file_1d(
    config: Settings, series: modin.Series, summary: dict
) -> Tuple[Settings, modin.Series, dict]:
    return pandas_describe_file_1d(config, series, summary)
