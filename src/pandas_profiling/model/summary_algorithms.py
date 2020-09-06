from typing import Tuple
from urllib.parse import urlsplit

import numpy as np
import pandas as pd
from pandas.api.types import is_categorical_dtype
from pandas.core.arrays.integer import _IntegerDtype

from pandas_profiling.config import config
from pandas_profiling.model.summary_helpers import (
    chi_square,
    file_summary,
    histogram_compute,
    image_summary,
    length_summary,
    path_summary,
    unicode_summary,
    url_summary,
)


def describe_counts(series: pd.Series, summary: dict) -> Tuple[pd.Series, dict]:
    """Counts the values in a series (with and without NaN, distinct).

    Args:
        series: Series for which we want to calculate the values.

    Returns:
        A dictionary with the count values (with and without NaN, distinct).
    """
    if is_categorical_dtype(series):
        series = series.cat.remove_unused_categories()

    # TODO: how bad do we need all of this?
    value_counts_with_nan = series.value_counts(dropna=False)
    # TODO: keep NaN counts...
    value_counts_without_nan = (
        value_counts_with_nan.reset_index().dropna().set_index("index").iloc[:, 0]
    )

    summary.update(
        {
            "value_counts_without_nan": value_counts_without_nan,
        }
    )

    return series, summary


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
    distinct_count = value_counts.count()
    unique_count = value_counts.where(value_counts == 1).count()

    stats = {
        "n_distinct": distinct_count,
        "p_distinct": distinct_count / count,
        "is_unique": unique_count == count,
        "n_unique": unique_count,
        "p_unique": unique_count / count,
    }
    stats.update(series_description)

    return series, stats


def describe_unsupported(series: pd.Series, summary: dict) -> Tuple[pd.Series, dict]:
    """Describe an unsupported series.
    Args:
        series: The Series to describe.
        summary: The dict containing the series description so far.
    Returns:
        A dict containing calculated series description values.
    """

    # number of observations in the Series
    length = len(series)

    # number of non-NaN observations in the Series
    count = series.count()

    summary.update(
        {
            "n": length,
            "count": count,
            # TODO: use value count NaN?
            "n_missing": length - count,
            "p_missing": 1 - count / length,
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


def numeric_stats_numpy(present_values, series, series_description):
    return {
        "mean": np.mean(present_values),
        "std": np.std(present_values, ddof=1),
        "variance": np.var(present_values, ddof=1),
        "min": np.min(present_values),
        "max": np.max(present_values),
        # Unbiased kurtosis obtained using Fisher's definition (kurtosis of normal == 0.0). Normalized by N-1.
        "kurtosis": series.kurt(),
        # Unbiased skew normalized by N-1
        "skewness": series.skew(),
        "sum": np.sum(present_values),
        "n_zeros": (series_description["count"] - np.count_nonzero(present_values)),
    }


def describe_numeric_1d(series: pd.Series, summary: dict) -> Tuple[pd.Series, dict]:
    """Describe a numeric series.
    Args:
        series: The Series to describe.
        series_description: The dict containing the series description so far.
    Returns:
        A dict containing calculated series description values.
    """

    def mad(arr):
        """Median Absolute Deviation: a "Robust" version of standard deviation.
        Indices variability of the sample.
        https://en.wikipedia.org/wiki/Median_absolute_deviation
        """
        return np.median(np.abs(arr - np.median(arr)))

    # Config
    chi_squared_threshold = config["vars"]["num"]["chi_squared_threshold"].get(float)
    quantiles = config["vars"]["num"]["quantiles"].get(list)

    n_infinite = ((series == np.inf) | (series == -np.inf)).sum()

    stats = summary

    if isinstance(series.dtype, _IntegerDtype):
        stats.update(numeric_stats_pandas(series))
        present_values = series.loc[series.notnull()].astype(str(series.dtype).lower())
        stats["n_zeros"] = summary["count"] - np.count_nonzero(present_values)
        finite_values = present_values
    else:
        values = series.values
        present_values = values[~np.isnan(values)]
        finite_values = values[np.isfinite(values)]
        stats.update(numeric_stats_numpy(present_values, series, summary))

    stats.update(
        {
            "mad": mad(present_values),
            "p_infinite": n_infinite / summary["n"],
            "n_infinite": n_infinite,
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

    stats["monotonic_increase"] = series.is_monotonic_increasing
    stats["monotonic_decrease"] = series.is_monotonic_decreasing

    stats["monotonic_increase_strict"] = (
        stats["monotonic_increase"] and series.is_unique
    )
    stats["monotonic_decrease_strict"] = (
        stats["monotonic_decrease"] and series.is_unique
    )

    stats.update(histogram_compute(finite_values, summary["n_distinct"]))
    return series, stats


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

    values = series[series.notnull()].values.astype(np.int64) // 10 ** 9

    if chi_squared_threshold > 0.0:
        summary["chi_squared"] = chi_square(values)

    summary.update(histogram_compute(values, summary["n_distinct"]))
    return values, summary


def describe_categorical_1d(series: pd.Series, summary: dict) -> Tuple[pd.Series, dict]:
    """Describe a categorical series.

    Args:
        series: The Series to describe.
        summary: The dict containing the series description so far.

    Returns:
        A dict containing calculated series description values.
    """
    chi_squared_threshold = config["vars"]["num"]["chi_squared_threshold"].get(float)
    check_length = config["vars"]["cat"]["length"].get(bool)
    check_unicode = config["vars"]["cat"]["unicode"].get(bool)
    # coerce_str_to_date = config["vars"]["cat"]["coerce_str_to_date"].get(bool)

    # Make sure we deal with strings (Issue #100)
    series = series[series.notna()].astype(str)

    # Only run if at least 1 non-missing value
    value_counts = summary["value_counts_without_nan"]

    summary.update(
        histogram_compute(
            value_counts, summary["n_distinct"], name="histogram_frequencies"
        )
    )

    if chi_squared_threshold > 0.0:
        summary["chi_squared"] = chi_square(histogram=value_counts.values)

    if check_length:
        summary.update(length_summary(series))
        summary.update(
            histogram_compute(
                summary["length"], summary["length"].nunique(), name="histogram_length"
            )
        )

    if check_unicode:
        summary.update(unicode_summary(series))

    # TODO: visions!
    # if coerce_str_to_date:
    #     summary["date_warning"] = warning_type_date(series)

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
        series_description: The dict containing the series description so far.

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
