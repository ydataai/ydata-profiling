from typing import Tuple

from ydata_profiling.config import Settings
from ydata_profiling.model.pandas.describe_image_pandas import pandas_describe_image_1d
from ydata_profiling.model.summary_algorithms import describe_image_1d
from ydata_profiling.utils import modin
from ydata_profiling.utils.imghdr_patch import *  # noqa: F401,F403


@describe_image_1d.register
def modin_describe_image_1d(
    config: Settings, series: modin.Series, summary: dict
) -> Tuple[Settings, modin.Series, dict]:
    return pandas_describe_image_1d(config, series, summary)
