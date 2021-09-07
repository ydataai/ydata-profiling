import os
from typing import Tuple

import pandas as pd

from pandas_profiling.config import Settings
from pandas_profiling.model.schema import PathColumnResult
from pandas_profiling.model.summary_algorithms import describe_path_1d


def path_summary(series: pd.Series) -> PathColumnResult:
    """

    Args:
        series: series to summarize

    Returns:

    """

    result = PathColumnResult()
    result.common_prefix = (
        os.path.commonprefix(series.values.tolist()) or "No common prefix"
    )

    # TODO: optimize using value counts
    result.stem_counts = series.map(lambda x: os.path.splitext(x)[0]).value_counts()
    result.suffix_counts = series.map(lambda x: os.path.splitext(x)[1]).value_counts()
    result.name_counts = series.map(lambda x: os.path.basename(x)).value_counts()
    result.parent_counts = series.map(lambda x: os.path.dirname(x)).value_counts()
    result.anchor_counts = series.map(lambda x: os.path.splitdrive(x)[0]).value_counts()

    result.n_stem_unique = len(result.stem_counts)
    result.n_suffix_unique = len(result.suffix_counts)
    result.n_name_unique = len(result.name_counts)
    result.n_parent_unique = len(result.parent_counts)
    result.n_anchor_unique = len(result.anchor_counts)

    return result


@describe_path_1d.register
def pandas_describe_path_1d(
    config: Settings, series: pd.Series, summary: dict
) -> Tuple[Settings, pd.Series, PathColumnResult]:
    """Describe a path series.

    Args:
        config: report Settings object
        series: The Series to describe.
        summary: The dict containing the series description so far.

    Returns:
        A dict containing calculated series description values.
    """

    # Make sure we deal with strings (Issue #100)
    if series.hasnans:
        raise ValueError("May not contain NaNs")
    if not hasattr(series, "str"):
        raise ValueError("series should have .str accessor")

    result = path_summary(series)

    return config, series, result
