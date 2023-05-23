from typing import Tuple

from ydata_profiling.config import Settings
from ydata_profiling.model.pandas.describe_supported_pandas import (
    pandas_describe_supported,
)
from ydata_profiling.model.summary_algorithms import describe_supported, series_hashable
from ydata_profiling.utils import modin


@describe_supported.register
@series_hashable
def modin_describe_supported(
    config: Settings, series: modin.Series, series_description: dict
) -> Tuple[Settings, modin.Series, dict]:
    return pandas_describe_supported(config, series, series_description)
