from typing import Tuple

from ydata_profiling.config import Settings
from ydata_profiling.model.pandas.describe_counts_pandas import pandas_describe_counts
from ydata_profiling.model.summary_algorithms import describe_counts
from ydata_profiling.utils import modin


@describe_counts.register
def modin_describe_counts(
    config: Settings, series: modin.Series, summary: dict
) -> Tuple[Settings, modin.Series, dict]:
    return pandas_describe_counts(config, series, summary)
