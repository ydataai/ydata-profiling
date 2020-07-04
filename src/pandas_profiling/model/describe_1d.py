import warnings
from pathlib import Path
from typing import Callable, Mapping, Tuple
from urllib.parse import urlsplit

import numpy as np
from scipy.stats.stats import chisquare

from visions.application.summaries.series import (
    file_summary,
    image_summary,
    path_summary,
    url_summary,
)

from pandas_profiling.config import config as config
from pandas_profiling.model.messages import (
    check_correlation_messages,
    check_table_messages,
    check_variable_messages,
    warning_type_date,
)


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

    distinct_count = series_description["distinct_count_without_nan"]

    stats = {
        "n": length,
        "count": count,
        "distinct_count": distinct_count,
        "n_unique": distinct_count,
        "p_missing": 1 - (count / length),
        "n_missing": length - count,
        "is_unique": distinct_count == count,
        "mode": series.mode().iloc[0] if count > distinct_count > 1 else series[0],
        "p_unique": distinct_count / count,
        "memory_size": series.memory_usage(config["memory_deep"].get(bool)),
    }

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

    values = series.values
    present_values = values[~np.isnan(values)]
    finite_values = values[np.isfinite(values)]

    stats = {
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
        "mad": mad(present_values),
        "n_zeros": (series_description["count"] - np.count_nonzero(present_values)),
        "histogram_data": finite_values,
        "scatter_data": series,  # For complex
        "p_infinite": n_infinite / series_description["n"],
        "n_infinite": n_infinite,
    }

    chi_squared_threshold = config["vars"]["num"]["chi_squared_threshold"].get(
        float
    )
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

    bins = config["plot"]["histogram"]["bins"].get(int)
    # Bins should never be larger than the number of distinct values
    bins = min(series_description["distinct_count_with_nan"], bins)
    stats["histogram_bins"] = bins

    bayesian_blocks_bins = config["plot"]["histogram"]["bayesian_blocks_bins"].get(
        bool
    )
    if bayesian_blocks_bins:
        from astropy.stats import bayesian_blocks

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            ret = bayesian_blocks(stats["histogram_data"])

            # Sanity check
            if not np.isnan(ret).any() and ret.size > 1:
                stats["histogram_bins_bayesian_blocks"] = ret

    return stats

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
        "histogram_data": series,
    }

    bins = config["plot"]["histogram"]["bins"].get(int)
    # Bins should never be larger than the number of distinct values
    bins = min(series_description["distinct_count_with_nan"], bins)
    stats["histogram_bins"] = bins

    stats["range"] = stats["max"] - stats["min"]

    chi_squared_threshold = config["vars"]["num"]["chi_squared_threshold"].get(
        float
    )
    if chi_squared_threshold > 0.0:
        histogram = np.histogram(
            series[series.notna()].astype("int64").values, bins="auto"
        )[0]
        stats["chi_squared"] = chisquare(histogram)

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

    chi_squared_threshold = config["vars"]["num"]["chi_squared_threshold"].get(
        float
    )
    if chi_squared_threshold > 0.0:
        stats["chi_squared"] = list(chisquare(value_counts.values))

    check_length = config["vars"]["cat"]["length"].get(bool)
    if check_length:
        from visions.application.summaries.series.text_summary import length_summary

        stats.update(length_summary(series))

    check_unicode = config["vars"]["cat"]["unicode"].get(bool)
    if check_unicode:
        from visions.application.summaries.series.text_summary import (
            unicode_summary,
        )

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

    # TODO: distinct counts for file_sizes
    bins = config["plot"]["histogram"]["bins"].get(int)
    bins = min(series_description["distinct_count_with_nan"], bins)
    stats["histogram_bins"] = bins

    series_description.update(describe_path_1d(series, series_description))

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
    # Make sure pd.NA is not in the series