from typing import Tuple

from ydata_profiling.config import Settings
from ydata_profiling.model.pandas.describe_text_pandas import pandas_describe_text_1d
from ydata_profiling.model.summary_algorithms import (
    describe_text_1d,
    series_handle_nulls,
    series_hashable,
)
from ydata_profiling.utils import modin


@describe_text_1d.register
@series_hashable
@series_handle_nulls
def modin_describe_text_1d(
    config: Settings, series: modin.Series, summary: dict
) -> Tuple[Settings, modin.Series, dict]:
    return pandas_describe_text_1d(config, series, summary)
