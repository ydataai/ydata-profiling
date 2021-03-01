import functools
from typing import Tuple
from urllib.parse import urlsplit

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
    except:
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

    return inner


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
        "is_unique": unique_count == count,
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
            "p_missing": summary["n_missing"] / length,
            "count": length - summary["n_missing"],
            "memory_size": series.memory_usage(deep=config["memory_deep"].get(bool)),
        }
    )

    return series, summary


def numeric_stats_pandas(series: pd.Series):
    #     summary["min"] = summary["value_counts_without_nan"].index.min()
    # vc.index.min()
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


def numeric_stats_numpy(present_values, series, series_description):
    vc = series_description["value_counts_without_nan"]
    index_values = vc.index.values
    return {
        "mean": np.mean(present_values),
        "std": np.std(present_values, ddof=1),
        "variance": np.var(present_values, ddof=1),
        "min": np.min(index_values),
        "max": np.max(index_values),
        # Unbiased kurtosis obtained using Fisher's definition (kurtosis of normal == 0.0). Normalized by N-1.
        "kurtosis": series.kurt(),
        # Unbiased skew normalized by N-1
        "skewness": series.skew(),
        "sum": np.sum(present_values),
    }


@series_hashable
@func_nullable_series_contains
def describe_numeric_1d(series: pd.Series, summary: dict) -> Tuple[pd.Series, dict]:
    """Describe a numeric series.
    Args:
        series: The Series to describe.
        summary: The dict containing the series description so far.
    Returns:
        A dict containing calculated series description values.
    """

    # Config
    chi_squared_threshold = config["vars"]["num"]["chi_squared_threshold"].get(float)
    quantiles = config["vars"]["num"]["quantiles"].get(list)

    value_counts = summary["value_counts_without_nan"]

    summary["n_zeros"] = 0
    negative_index = value_counts.index < 0
    summary["n_negative"] = value_counts.loc[negative_index].sum()
    summary["p_negative"] = summary["n_negative"] / summary["n"]

    infinity_values = [np.inf, -np.inf]
    infinity_index = value_counts.index.isin(infinity_values)
    summary["n_infinite"] = value_counts.loc[infinity_index].sum()

    if 0 in value_counts.index:
        summary["n_zeros"] = value_counts.loc[0]

    stats = summary

    if isinstance(series.dtype, _IntegerDtype):
        stats.update(numeric_stats_pandas(series))
        present_values = series.astype(str(series.dtype).lower())
        finite_values = present_values
    else:
        present_values = series.values
        finite_values = present_values[np.isfinite(present_values)]
        stats.update(numeric_stats_numpy(present_values, series, summary))

    stats.update(
        {
            "mad": mad(present_values),
        }
    )

    if chi_squared_threshold > 0.0:
        stats["chi_squared"] = chi_square(finite_values)

    stats["range"] = stats["max"] - stats["min"]
    stats.update(
        {
            f"{percentile:.0%}": value
            for percentile, value in series.quantile(quantiles).to_dict().items()
        }
    )
    stats["iqr"] = stats["75%"] - stats["25%"]
    stats["cv"] = stats["std"] / stats["mean"] if stats["mean"] else np.NaN
    stats["p_zeros"] = stats["n_zeros"] / summary["n"]
    stats["p_infinite"] = summary["n_infinite"] / summary["n"]

    stats["monotonic_increase"] = series.is_monotonic_increasing
    stats["monotonic_decrease"] = series.is_monotonic_decreasing

    stats["monotonic_increase_strict"] = (
        stats["monotonic_increase"] and series.is_unique
    )
    stats["monotonic_decrease_strict"] = (
        stats["monotonic_decrease"] and series.is_unique
    )

    stats.update(
        histogram_compute(
            value_counts[~infinity_index].index.values,
            summary["n_distinct"],
            weights=value_counts[~infinity_index].values,
        )
    )

    return series, stats


@series_hashable
@func_nullable_series_contains
def describe_date_1d(series: pd.Series, summary: dict) -> Tuple[pd.Series, dict]:
    """Describe a date series.

    Args:
        series: The Series to describe.
        summary: The dict containing the series description so far.

    Returns:
        A dict containing calculated series description values.
    """
    chi_squared_threshold = config["vars"]["num"]["chi_squared_threshold"].get(float)

    summary.update(
        {
            "min": pd.Timestamp.to_pydatetime(series.min()),
            "max": pd.Timestamp.to_pydatetime(series.max()),
        }
    )

    summary["range"] = summary["max"] - summary["min"]

    values = series.values.astype(np.int64) // 10 ** 9

    if chi_squared_threshold > 0.0:
        summary["chi_squared"] = chi_square(values)

    summary.update(histogram_compute(values, summary["n_distinct"]))
    return values, summary


@series_hashable
@func_nullable_series_contains
def describe_categorical_1d(series: pd.Series, summary: dict) -> Tuple[pd.Series, dict]:
    """Describe a categorical series.

    Args:
        series: The Series to describe.
        summary: The dict containing the series description so far.

    Returns:
        A dict containing calculated series description values.
    """

    # Make sure we deal with strings (Issue #100)
    series = series.astype(str)

    # Only run if at least 1 non-missing value
    value_counts = summary["value_counts_without_nan"]

    summary.update(
        histogram_compute(
            value_counts, summary["n_distinct"], name="histogram_frequencies"
        )
    )

    redact = config["vars"]["cat"]["redact"].get(float)
    if not redact:
        summary.update({"first_rows": series.head(5)})

    chi_squared_threshold = config["vars"]["num"]["chi_squared_threshold"].get(float)
    if chi_squared_threshold > 0.0:
        summary["chi_squared"] = chi_square(histogram=value_counts.values)

    check_length = config["vars"]["cat"]["length"].get(bool)
    if check_length:
        summary.update(length_summary(series))
        summary.update(
            histogram_compute(
                summary["length"], summary["length"].nunique(), name="histogram_length"
            )
        )

    check_unicode = config["vars"]["cat"]["characters"].get(bool)
    if check_unicode:
        summary.update(unicode_summary(series))
        summary["n_characters_distinct"] = summary["n_characters"]
        summary["n_characters"] = summary["character_counts"].values.sum()

        try:
            summary["category_alias_counts"].index = summary[
                "category_alias_counts"
            ].index.str.replace("_", " ")
        except AttributeError:
            pass

    words = config["vars"]["cat"]["words"]
    if words:
        summary.update(word_summary(series))

    return series, summary


def describe_url_1d(series: pd.Series, summary: dict) -> Tuple[pd.Series, dict]:
    """Describe a url series.

    Args:
        series: The Series to describe.
        summary: The dict containing the series description so far.

    Returns:
        A dict containing calculated series description values.
    """

    # Make sure we deal with strings (Issue #100)
    assert not series.hasnans
    assert hasattr(series, "str")

    # Transform
    series = series.apply(urlsplit)

    # Update
    summary.update(url_summary(series))

    return series, summary


def describe_file_1d(series: pd.Series, summary: dict) -> Tuple[pd.Series, dict]:
    assert not series.hasnans
    assert hasattr(series, "str")

    summary.update(file_summary(series))
    summary.update(
        histogram_compute(
            summary["file_size"],
            summary["file_size"].nunique(),
            name="histogram_file_size",
        )
    )

    return series, summary


def describe_path_1d(series: pd.Series, summary: dict) -> Tuple[pd.Series, dict]:
    """Describe a path series.

    Args:
        series: The Series to describe.
        summary: The dict containing the series description so far.

    Returns:
        A dict containing calculated series description values.
    """

    # Make sure we deal with strings (Issue #100)
    assert not series.hasnans
    assert hasattr(series, "str")

    summary.update(path_summary(series))

    return series, summary


def describe_image_1d(series: pd.Series, summary: dict) -> Tuple[pd.Series, dict]:
    assert not series.hasnans
    assert hasattr(series, "str")

    extract_exif = config["vars"]["image"]["exif"].get(bool)

    summary.update(image_summary(series, extract_exif))

    return series, summary


@series_hashable
def describe_boolean_1d(series: pd.Series, summary: dict) -> Tuple[pd.Series, dict]:
    """Describe a boolean series.

    Args:
        series: The Series to describe.
        summary: The dict containing the series description so far.

    Returns:
        A dict containing calculated series description values.
    """

    value_counts = summary["value_counts_without_nan"]
    summary.update({"top": value_counts.index[0], "freq": value_counts.iloc[0]})

    return series, summary
