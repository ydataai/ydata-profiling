import os
from datetime import datetime
from typing import Tuple

import pandas as pd

from pandas_profiling.config import Settings
from pandas_profiling.model.schema import FileColumnResult
from pandas_profiling.model.summary_algorithms import (
    describe_file_1d,
    histogram_compute,
)


def file_summary(series: pd.Series) -> FileColumnResult:
    """

    Args:
        series: series to summarize

    Returns:

    """

    # Transform
    stats = series.map(lambda x: os.stat(x))

    def convert_datetime(x: float) -> str:
        return datetime.fromtimestamp(x).strftime("%Y-%m-%d %H:%M:%S")

    # Transform some more
    result = FileColumnResult()
    result.file_size = stats.map(lambda x: x.st_size)
    result.file_created_time = stats.map(lambda x: x.st_ctime).map(convert_datetime)
    result.file_accessed_time = stats.map(lambda x: x.st_atime).map(convert_datetime)
    result.file_modified_time = stats.map(lambda x: x.st_mtime).map(convert_datetime)

    return result


@describe_file_1d.register
def pandas_describe_file_1d(
    config: Settings, series: pd.Series, summary: dict
) -> Tuple[Settings, pd.Series, FileColumnResult]:
    if series.hasnans:
        raise ValueError("May not contain NaNs")
    if not hasattr(series, "str"):
        raise ValueError("series should have .str accessor")

    result = file_summary(series)
    r = histogram_compute(
        config,
        result.file_size,
        result.file_size.nunique(),
        name="histogram_file_size",
    )
    result.histogram_file_size = r["histogram_file_size"]

    return config, series, result
