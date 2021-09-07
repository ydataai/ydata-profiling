from typing import Tuple
from urllib.parse import urlsplit

import pandas as pd

from pandas_profiling.config import Settings
from pandas_profiling.model.schema import UrlColumnResult
from pandas_profiling.model.summary_algorithms import describe_url_1d


def url_summary(series: pd.Series) -> UrlColumnResult:
    """

    Args:
        series: series to summarize

    Returns:

    """
    result = UrlColumnResult()
    result.scheme_counts = series.map(lambda x: x.scheme).value_counts()
    result.netloc_counts = series.map(lambda x: x.netloc).value_counts()
    result.path_counts = series.map(lambda x: x.path).value_counts()
    result.query_counts = series.map(lambda x: x.query).value_counts()
    result.fragment_counts = series.map(lambda x: x.fragment).value_counts()

    return result


@describe_url_1d.register
def pandas_describe_url_1d(
    config: Settings, series: pd.Series, summary: dict
) -> Tuple[Settings, pd.Series, UrlColumnResult]:
    """Describe a url series.

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

    # Transform
    series = series.apply(urlsplit)

    # Update
    result = url_summary(series)

    return config, series, result
