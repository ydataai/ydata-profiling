from typing import Tuple

from ydata_profiling.config import Settings
from ydata_profiling.model.pandas.describe_boolean_pandas import (
    pandas_describe_boolean_1d,
)
from ydata_profiling.model.summary_algorithms import (
    describe_boolean_1d,
    series_hashable,
)
from ydata_profiling.utils import modin


@describe_boolean_1d.register
@series_hashable
def modin_describe_boolean_1d(
    config: Settings, series: modin.Series, summary: dict
) -> Tuple[Settings, modin.Series, dict]:
    return pandas_describe_boolean_1d(config, series, summary)
