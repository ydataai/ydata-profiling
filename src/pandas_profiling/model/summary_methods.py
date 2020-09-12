from pathlib import Path
from urllib.parse import urlsplit

import numpy as np
import pandas as pd
from pandas.core.arrays.integer import _IntegerDtype
from scipy.stats.stats import chisquare
from visions.application.summaries.series import (
    file_summary,
    image_summary,
    path_summary,
    url_summary,
)
from visions.application.summaries.series.text_summary import (
    length_summary,
    unicode_summary,
)

from pandas_profiling.config import config as config
from pandas_profiling.model.messages import warning_type_date


def describe_supported(series: pd.Series, series_description: dict) -> dict:
    """Describe a supported series.
    Args:
        series: The Series to describe.
        series_description: The dict containing the series description so far.
    Returns:
        A dict containing calculated series description values.
    """

    # number of observations in the Series
    length = len(series)

    # number of non-NaN observations in the Series
    count = series.count()
    stats = {
        "n": length,
        "count": count,
        "p_missing": 1 - (count / length),
        "n_missing": length - count,
        "memory_size": series.memory_usage(config["memory_deep"].get(bool)),
    }

    distinct_count = series_description.get("distinct_count_without_nan", None)
    if distinct_count is not None:
        stats.update({
            "n_distinct": distinct_count,
            "p_distinct": distinct_count / count,
        })

    value_counts = series_description.get("value_counts_without_nan", None)
    if value_counts is not None:
        unique_count = value_counts.where(value_counts == 1).count()
        stats.update({
            "is_unique": unique_count == count,
            "n_unique": unique_count,
            "p_unique": unique_count / count,
        })

    return stats


def describe_unsupported(series: pd.Series, series_description: dict):
    """Describe an unsupported series.
    Args:
        series: The Series to describe.
        series_description: The dict containing the series description so far.
    Returns:
        A dict containing calculated series description values.
    """

    # number of observations in the Series
    length = len(series)

    # number of non-NaN observations in the Series
    count = series.count()

    results_data = {
        "n": length,
        "count": count,
        "p_missing": 1 - count / length,
        "n_missing": length - count,
        "memory_size": series.memory_usage(deep=config["memory_deep"].get(bool)),
    }

    return results_data


def histogram_compute(finite_values, n_unique, name="histogram"):
    stats = {}
    bins = config["plot"]["histogram"]["bins"].get(int)
    bins = "auto" if bins == 0 else min(bins, n_unique)
    stats[name] = np.histogram(finite_values, bins)

    max_bins = config["plot"]["histogram"]["max_bins"].get(int)
    if bins == "auto" and len(stats[name][1]) > max_bins:
        stats[name] = np.histogram(finite_values, max_bins)

    return stats


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


def numeric_stats_numpy(series, series_description):
    present_values = series[~np.isnan(series)]
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


def describe_numeric_1d(series: pd.Series, series_description: dict) -> dict:
    """Describe a numeric series.
    Args:
        series: The Series to describe.
        series_description: The dict containing the series description so far.
    Returns:
        A dict containing calculated series description values.
    Notes:
        When 'bins_type' is set to 'bayesian_blocks', astropy.stats.bayesian_blocks is used to determine the number of
        bins. Read the docs:
        https://docs.astropy.org/en/stable/visualization/histogram.html
        https://docs.astropy.org/en/stable/api/astropy.stats.bayesian_blocks.html
        This method might print warnings, which we suppress.
        https://github.com/astropy/astropy/issues/4927
    """

    def mad(arr):
        """ Median Absolute Deviation: a "Robust" version of standard deviation.
            Indices variability of the sample.
            https://en.wikipedia.org/wiki/Median_absolute_deviation
        """
        return np.median(np.abs(arr - np.median(arr)))

    quantiles = config["vars"]["num"]["quantiles"].get(list)

    n_infinite = ((series == np.inf) | (series == -np.inf)).sum()

    if isinstance(series.dtype, _IntegerDtype):
        stats = numeric_stats_pandas(series)
        present_values = series.loc[series.notnull()].astype(str(series.dtype).lower())
        stats["n_zeros"] = series_description["count"] - np.count_nonzero(
            present_values
        )
        stats["histogram_data"] = present_values
        finite_values = present_values
    else:
        values = series.values
        present_values = values[~np.isnan(values)]
        finite_values = values[np.isfinite(values)]
        stats = numeric_stats_numpy(series, series_description)
        stats["histogram_data"] = finite_values

    stats.update(
        {
            "mad": mad(present_values),
            "scatter_data": series,  # For complex
            "p_infinite": n_infinite / series_description["n"],
            "n_infinite": n_infinite,
        }
    )

    chi_squared_threshold = config["vars"]["num"]["chi_squared_threshold"].get(float)
    if chi_squared_threshold > 0.0:
        histogram, _ = np.histogram(finite_values, bins="auto")
        stats["chi_squared"] = chisquare(histogram)

    stats["range"] = stats["max"] - stats["min"]
    stats.update(
        {
            f"{percentile:.0%}": value
            for percentile, value in series.quantile(quantiles).to_dict().items()
        }
    )
    stats["iqr"] = stats["75%"] - stats["25%"]
    stats["cv"] = stats["std"] / stats["mean"] if stats["mean"] else np.NaN
    stats["p_zeros"] = stats["n_zeros"] / series_description["n"]

    stats["monotonic_increase"] = series.is_monotonic_increasing
    stats["monotonic_decrease"] = series.is_monotonic_decreasing

    stats["monotonic_increase_strict"] = (
        stats["monotonic_increase"] and series.is_unique
    )
    stats["monotonic_decrease_strict"] = (
        stats["monotonic_decrease"] and series.is_unique
    )

    stats.update(histogram_compute(finite_values, series_description["n_distinct"]))

    return stats


def describe_complex_1d(series: pd.Series, series_description: dict) -> dict:
    return describe_numeric_1d(series, series_description)


def describe_date_1d(series: pd.Series, series_description: dict) -> dict:
    """Describe a date series.

    Args:
        series: The Series to describe.
        series_description: The dict containing the series description so far.

    Returns:
        A dict containing calculated series description values.
    """
    stats = {
        "min": pd.Timestamp.to_pydatetime(series.min()),
        "max": pd.Timestamp.to_pydatetime(series.max()),
    }

    stats["range"] = stats["max"] - stats["min"]

    values = series[series.notnull()].values.astype(np.int64) // 10 ** 9

    chi_squared_threshold = config["vars"]["num"]["chi_squared_threshold"].get(float)
    if chi_squared_threshold > 0.0:
        histogram, _ = np.histogram(values, bins="auto")
        stats["chi_squared"] = chisquare(histogram)

    stats.update(histogram_compute(values, series_description["n_unique"]))
    return stats


def describe_categorical_1d(series: pd.Series, series_description: dict) -> dict:
    """Describe a categorical series.
    Args:
        series: The Series to describe.
        series_description: The dict containing the series description so far.
    Returns:
        A dict containing calculated series description values.
    """
    # Make sure we deal with strings (Issue #100)
    series = series.astype(str)

    # Only run if at least 1 non-missing value
    value_counts = series_description["value_counts_without_nan"]

    stats = {"top": value_counts.index[0], "freq": value_counts.iloc[0]}

    stats.update(
        histogram_compute(
            value_counts, len(value_counts), name="histogram_frequencies"
        )
    )

    chi_squared_threshold = config["vars"]["num"]["chi_squared_threshold"].get(
        float
    )
    if chi_squared_threshold > 0.0:
        stats["chi_squared"] = list(chisquare(value_counts.values))

    check_length = config["vars"]["cat"]["length"].get(bool)
    if check_length:
        stats.update(length_summary(series))
        stats.update(
            histogram_compute(
                stats["length"], stats["length"].nunique(), name="histogram_length"
            )
        )

    check_unicode = config["vars"]["cat"]["unicode"].get(bool)
    if check_unicode:
        stats.update(unicode_summary(series))

        stats["category_alias_counts"].index = stats[
            "category_alias_counts"
        ].index.str.replace("_", " ")

    coerce_str_to_date = config["vars"]["cat"]["coerce_str_to_date"].get(bool)
    if coerce_str_to_date:
        stats["date_warning"] = warning_type_date(series)

    return stats


def describe_url_1d(series: pd.Series, series_description: dict) -> dict:
    """Describe a url series.

    Args:
        series: The Series to describe.
        series_description: The dict containing the series description so far.

    Returns:
        A dict containing calculated series description values.
    """
    # Make sure we deal with strings (Issue #100)
    series = series[~series.isnull()].astype(str)
    series = series.apply(urlsplit)

    stats = url_summary(series)

    # Only run if at least 1 non-missing value
    value_counts = series_description["value_counts_without_nan"]

    stats["top"] = value_counts.index[0]
    stats["freq"] = value_counts.iloc[0]

    return stats


def describe_file_1d(series: pd.Series, series_description: dict) -> dict:
    if "p_series" not in series_description:
        series = series[~series.isnull()].astype(str)
        series = series.map(Path)
        series_description["p_series"] = series
    else:
        series = series_description["p_series"]

    stats = file_summary(series)

    series_description.update(describe_path_1d(series, series_description))
    stats.update(
        histogram_compute(
            stats["file_size"],
            stats["file_size"].nunique(),
            name="histogram_file_size",
        )
    )

    return stats


def describe_path_1d(series: pd.Series, series_description: dict) -> dict:
    """Describe a path series.

    Args:
        series: The Series to describe.
        series_description: The dict containing the series description so far.

    Returns:
        A dict containing calculated series description values.
    """
    series_description.update(describe_categorical_1d(series, series_description))

    # Make sure we deal with strings (Issue #100)
    if "p_series" not in series_description:
        series = series[~series.isnull()].astype(str)
        series = series.map(Path)
    else:
        series = series_description["p_series"]
        del series_description["p_series"]

    stats = path_summary(series)

    # Only run if at least 1 non-missing value
    value_counts = series_description["value_counts_without_nan"]

    stats["top"] = value_counts.index[0]
    stats["freq"] = value_counts.iloc[0]

    return stats


def describe_image_1d(series: pd.Series, series_description: dict):
    if "p_series" not in series_description:
        series = series[~series.isnull()].astype(str)
        series = series.map(Path)
        series_description["p_series"] = series
    else:
        series = series_description["p_series"]

    extract_exif = config["vars"]["image"]["exif"].get(bool)

    stats = image_summary(series, extract_exif)

    series_description.update(describe_file_1d(series, series_description))

    return stats


def describe_boolean_1d(series: pd.Series, series_description: dict) -> dict:
    """Describe a boolean series.

    Args:
        series: The Series to describe.
        series_description: The dict containing the series description so far.

    Returns:
        A dict containing calculated series description values.
    """
    value_counts = series_description["value_counts_without_nan"]

    stats = {"top": value_counts.index[0], "freq": value_counts.iloc[0]}

    return stats
