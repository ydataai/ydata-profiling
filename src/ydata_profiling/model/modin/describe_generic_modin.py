from typing import Tuple

from ydata_profiling.config import Settings
from ydata_profiling.model.pandas.describe_generic_pandas import pandas_describe_generic
from ydata_profiling.model.summary_algorithms import describe_generic
from ydata_profiling.utils import modin


@describe_generic.register
def modin_describe_generic(
    config: Settings, series: modin.Series, summary: dict
) -> Tuple[Settings, modin.Series, dict]:
    return pandas_describe_generic(config, series, summary)
