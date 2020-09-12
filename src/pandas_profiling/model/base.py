"""Common parts to all other modules, mainly utility functions."""
import pandas as pd
from pandas.api.types import is_categorical_dtype


def get_counts(series: pd.Series) -> dict:
    """Counts the values in a series (with and without NaN, distinct).

    Args:
        series: Series for which we want to calculate the values.

    Returns:
        A dictionary with the count values (with and without NaN, distinct).
    """

    if is_categorical_dtype(series):
        series = series.cat.remove_unused_categories()

    series_summary = {
        "hashable": True,
        "value_counts_with_nan": series.value_counts(dropna=False),
    }

    series_summary["value_counts_without_nan"] = (
        series_summary["value_counts_with_nan"]
        .reset_index()
        .dropna()
        .set_index("index")
        .iloc[:, 0]
    )

    series_summary["distinct_count_with_nan"] = series_summary[
        "value_counts_with_nan"
    ].count()
    series_summary["distinct_count_without_nan"] = series_summary[
        "value_counts_without_nan"
    ].count()

    # TODO: No need for duplication here, refactor
    series_summary["value_counts"] = series_summary["value_counts_without_nan"]
    try:
        set(series_summary["value_counts_with_nan"].index)
    except:
        series_summary["hashable"] = False

    return series_summary
