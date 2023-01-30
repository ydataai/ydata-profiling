from typing import Tuple

import pandas as pd

from ydata_profiling.config import Settings
from ydata_profiling.model.summary_algorithms import describe_counts


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
    try:
        value_counts_with_nan = series.value_counts(dropna=False)
        _ = set(value_counts_with_nan.index)
        hashable = True
    except:  # noqa: E722
        hashable = False

    summary["hashable"] = hashable

    if hashable:
        value_counts_with_nan = value_counts_with_nan[value_counts_with_nan > 0]

        null_index = value_counts_with_nan.index.isnull()
        if null_index.any():
            n_missing = value_counts_with_nan[null_index].sum()
            value_counts_without_nan = value_counts_with_nan[~null_index]
        else:
            n_missing = 0
            value_counts_without_nan = value_counts_with_nan

        summary.update(
            {
                "value_counts_without_nan": value_counts_without_nan,
            }
        )

        try:
            summary["value_counts_index_sorted"] = summary[
                "value_counts_without_nan"
            ].sort_index(ascending=True)
            ordering = True
        except TypeError:
            ordering = False
    else:
        n_missing = series.isna().sum()
        ordering = False

    summary["ordering"] = ordering
    summary["n_missing"] = n_missing

    return config, series, summary
