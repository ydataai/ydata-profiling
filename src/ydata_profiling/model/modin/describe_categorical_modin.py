from typing import Tuple

from ydata_profiling.config import Settings
from ydata_profiling.model.pandas.describe_categorical_pandas import (
    pandas_describe_categorical_1d,
)
from ydata_profiling.utils import modin


def modin_describe_categorical_1d(
    config: Settings, series: modin.Series, summary: dict
) -> Tuple[Settings, modin.Series, dict]:
    return pandas_describe_categorical_1d(config, series, summary)
