from typing import Tuple

from ydata_profiling.config import Settings
from ydata_profiling.model.pandas.describe_date_pandas import pandas_describe_date_1d
from ydata_profiling.model.summary_algorithms import (
    describe_date_1d,
    series_handle_nulls,
    series_hashable,
)
from ydata_profiling.utils import modin


@describe_date_1d.register
@series_hashable
@series_handle_nulls
def modin_describe_date_1d(
    config: Settings, series: modin.Series, summary: dict
) -> Tuple[Settings, modin.Series, dict]:
    return pandas_describe_date_1d(config, series, summary)
