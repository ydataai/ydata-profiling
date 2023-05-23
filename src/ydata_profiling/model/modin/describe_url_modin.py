from typing import Tuple

from ydata_profiling.config import Settings
from ydata_profiling.model.pandas.describe_url_pandas import pandas_describe_url_1d
from ydata_profiling.model.summary_algorithms import describe_url_1d
from ydata_profiling.utils import modin


@describe_url_1d.register
def modin_describe_url_1d(
    config: Settings, series: modin.Series, summary: dict
) -> Tuple[Settings, modin.Series, dict]:
    return pandas_describe_url_1d
