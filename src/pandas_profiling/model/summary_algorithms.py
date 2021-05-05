import contextlib
import functools
from typing import Any, Callable, Optional, Tuple, TypeVar

import numpy as np
import pandas as pd
from pandas.core.arrays.integer import _IntegerDtype
from visions.utils import func_nullable_series_contains

from pandas_profiling.config import config
from pandas_profiling.model.summary_helpers import (
    chi_square,
    file_summary,
    histogram_compute,
    image_summary,
    length_summary,
    mad,
    path_summary,
    unicode_summary,
    url_summary,
    word_summary,
)


def describe_counts(series: pd.Series, summary: dict) -> Tuple[pd.Series, dict]:
    """Counts the values in a series (with and without NaN, distinct).

    Args:
        series: Series for which we want to calculate the values.

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
    else:
        n_missing = series.isna().sum()

    summary["n_missing"] = n_missing

    return series, summary


def series_hashable(fn):
    @functools.wraps(fn)
    def inner(series, summary):
        if not summary["hashable"]:
            return series, summary
        return fn(series, summary)

from pandas_profiling.config import Settings

T = TypeVar("T")

@series_hashable
def describe_supported(
    series: pd.Series, series_description: dict
) -> Tuple[pd.Series, dict]:
    """Describe a supported series.
    Args:
        series: The Series to describe.
        series_description: The dict containing the series description so far.
    Returns:
        A dict containing calculated series description values.
    """

    # number of non-NaN observations in the Series
    count = series_description["count"]

    value_counts = series_description["value_counts_without_nan"]
    distinct_count = len(value_counts)
    unique_count = value_counts.where(value_counts == 1).count()

    stats = {
        "n_distinct": distinct_count,
        "p_distinct": distinct_count / count if count > 0 else 0,
        "is_unique": unique_count == count and count > 0,
        "n_unique": unique_count,
        "p_unique": unique_count / count if count > 0 else 0,
    }
    stats.update(series_description)

    return series, stats


def describe_generic(series: pd.Series, summary: dict) -> Tuple[pd.Series, dict]:
    """Describe generic series.
    Args:
        series: The Series to describe.
        summary: The dict containing the series description so far.
    Returns:
        A dict containing calculated series description values.
    """

    # number of observations in the Series
    length = len(series)

    summary.update(
        {
            "n": length,
            "p_missing": summary["n_missing"] / length if length > 0 else 0,
            "count": length - summary["n_missing"],
            "memory_size": series.memory_usage(deep=config["memory_deep"].get(bool)),
        }
    )

    return series, summary


def numeric_stats_pandas(series: pd.Series):
    return {
        "mean": series.mean(),
        "std": series.std(),
        "variance": series.var(),
        "min": series.min(),
        "max": series.max(),
        # Unbiased kurtosis obtained using Fisher's definition (kurtosis of normal == 0.0). Normalized by N-1.
        "kurtosis": series.kurt(),
        # Unbiased skew normalized by N-1
        "skewness": series.skew(),
        "sum": series.sum(),
    }

def func_nullable_series_contains(fn: Callable) -> Callable:
    @functools.wraps(fn)
    def inner(
        config: Settings, series: pd.Series, state: dict, *args, **kwargs
    ) -> bool:
        if series.hasnans:
            series = series.dropna()
            if series.empty:
                return False

        return fn(config, series, state, *args, **kwargs)

    return inner


def histogram_compute(
    config: Settings,
    finite_values: np.ndarray,
    n_unique: int,
    name: str = "histogram",
    weights: Optional[np.ndarray] = None,
) -> dict:
    stats = {}
    bins = config.plot.histogram.bins
    bins_arg = "auto" if bins == 0 else min(bins, n_unique)
    stats[name] = np.histogram(finite_values, bins=bins_arg, weights=weights)

    max_bins = config.plot.histogram.max_bins
    if bins_arg == "auto" and len(stats[name][1]) > max_bins:
        stats[name] = np.histogram(finite_values, bins=max_bins, weights=None)

    return stats


        with contextlib.suppress(AttributeError):
            summary["category_alias_counts"].index = summary[
                "category_alias_counts"
            ].index.str.replace("_", " ")


def series_hashable(
    fn: Callable[[Settings, pd.Series, dict], Tuple[Settings, pd.Series, dict]]
) -> Callable[[Settings, pd.Series, dict], Tuple[Settings, pd.Series, dict]]:
    @functools.wraps(fn)
    def inner(
        config: Settings, series: pd.Series, summary: dict
    ) -> Tuple[Settings, pd.Series, dict]:
        if not summary["hashable"]:
            return config, series, summary
        return fn(config, series, summary)

    return inner


def series_handle_nulls(
    fn: Callable[[Settings, pd.Series, dict], Tuple[Settings, pd.Series, dict]]
) -> Callable[[Settings, pd.Series, dict], Tuple[Settings, pd.Series, dict]]:
    """Decorator for nullable series"""

def func_nullable_series_contains(fn: Callable) -> Callable:
    @functools.wraps(fn)
    def inner(
        config: Settings, series: pd.Series, summary: dict
    ) -> Tuple[Settings, pd.Series, dict]:
        if series.hasnans:
            series = series.dropna()

        return fn(config, series, summary)

    return inner


def named_aggregate_summary(series: pd.Series, key: str) -> dict:
    summary = {
        f"max_{key}": np.max(series),
        f"mean_{key}": np.mean(series),
        f"median_{key}": np.median(series),
        f"min_{key}": np.min(series),
    }

    return summary


@multimethod
def describe_counts(
    config: Settings, series: Any, summary: dict
) -> Tuple[Settings, Any, dict]:
    raise NotImplementedError()


@multimethod
def describe_supported(
    config: Settings, series: Any, series_description: dict
) -> Tuple[Settings, Any, dict]:
    raise NotImplementedError()


@multimethod
def describe_generic(
    config: Settings, series: Any, summary: dict
) -> Tuple[Settings, Any, dict]:
    raise NotImplementedError()


@multimethod
def describe_numeric_1d(
    config: Settings, series: Any, summary: dict
) -> Tuple[Settings, Any, dict]:
    raise NotImplementedError()


@multimethod
def describe_date_1d(
    config: Settings, series: Any, summary: dict
) -> Tuple[Settings, Any, dict]:
    raise NotImplementedError()


@multimethod
def describe_categorical_1d(
    config: Settings, series: pd.Series, summary: dict
) -> Tuple[Settings, pd.Series, dict]:
    raise NotImplementedError()

def series_handle_nulls(
    fn: Callable[[Settings, pd.Series, dict], Tuple[Settings, pd.Series, dict]]
) -> Callable[[Settings, pd.Series, dict], Tuple[Settings, pd.Series, dict]]:
    """Decorator for nullable series"""

@multimethod
def describe_url_1d(
    config: Settings, series: Any, summary: dict
) -> Tuple[Settings, Any, dict]:
    raise NotImplementedError()

@multimethod
def describe_counts(
    config: Settings, series: Any, summary: dict
) -> Tuple[Settings, Any, dict]:
    raise NotImplementedError()

@multimethod
def describe_file_1d(
    config: Settings, series: Any, summary: dict
) -> Tuple[Settings, Any, dict]:
    raise NotImplementedError()

@multimethod
def describe_generic(
    config: Settings, series: Any, summary: dict
) -> Tuple[Settings, Any, dict]:
    raise NotImplementedError()

@multimethod
def describe_path_1d(
    config: Settings, series: Any, summary: dict
) -> Tuple[Settings, Any, dict]:
    raise NotImplementedError()

@multimethod
def describe_categorical_1d(
    config: Settings, series: pd.Series, summary: dict
) -> Tuple[Settings, pd.Series, dict]:
    raise NotImplementedError()

@multimethod
def describe_image_1d(
    config: Settings, series: Any, summary: dict
) -> Tuple[Settings, Any, dict]:
    raise NotImplementedError()


@multimethod
def describe_boolean_1d(
    config: Settings, series: Any, summary: dict
) -> Tuple[Settings, Any, dict]:
    raise NotImplementedError()
