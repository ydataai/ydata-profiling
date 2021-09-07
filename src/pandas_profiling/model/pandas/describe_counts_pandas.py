from typing import Tuple

import pandas as pd

from pandas_profiling.config import Settings
from pandas_profiling.model.schema import CountColumnResult
from pandas_profiling.model.summary_algorithms import describe_counts


@describe_counts.register
def pandas_describe_counts(
    config: Settings, series: pd.Series, summary: dict
) -> Tuple[Settings, pd.Series, dict]:
    """Counts the values in a series (with and without NaN, distinct).

    Args:
        config: report Settings object
        series: Series for which we want to calculate the values.
        summary: series' summary

    Returns:
        A dictionary with the count values (with and without NaN, distinct).
    """

    result = CountColumnResult()
    try:
        value_counts_with_nan = series.value_counts(dropna=False)
        _ = set(value_counts_with_nan.index)
        result.hashable = True
    except:  # noqa: E722
        result.hashable = False

    if result.hashable:
        value_counts_with_nan = value_counts_with_nan[value_counts_with_nan > 0]

        null_index = value_counts_with_nan.index.isnull()
        if null_index.any():
            result.n_missing = value_counts_with_nan[null_index].sum()
            value_counts_without_nan = value_counts_with_nan[~null_index]
        else:
            result.n_missing = 0
            value_counts_without_nan = value_counts_with_nan

        result.value_counts = value_counts_without_nan

        try:
            res = result.value_counts.sort_index(ascending=True)
            # ordering = True
            n_extreme_obs = config.n_extreme_obs

            result.values = res
        except TypeError:
            pass
            # ordering = False
    else:
        result.n_missing = series.isna().sum()
        # ordering = False

    return config, series, result
