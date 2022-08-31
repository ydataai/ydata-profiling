from typing import Any, Dict, Tuple

import numpy as np
import pandas as pd
from pandas.core.arrays.integer import _IntegerDtype

from pandas_profiling.config import Settings
from pandas_profiling.model.schema import Monotonicity, NumericColumnResult
from pandas_profiling.model.summary_algorithms import (
    chi_square,
    describe_numeric_1d,
    histogram_compute,
    series_handle_nulls,
    series_hashable,
)


def mad(arr: np.ndarray) -> np.ndarray:
    """Median Absolute Deviation: a "Robust" version of standard deviation.
    Indices variability of the sample.
    https://en.wikipedia.org/wiki/Median_absolute_deviation
    """
    return np.median(np.abs(arr - np.median(arr)))


def numeric_stats_pandas(series: pd.Series) -> Dict[str, Any]:
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


def numeric_stats_numpy(
    present_values: np.ndarray, series: pd.Series, series_description: Dict[str, Any]
) -> Dict[str, Any]:
    vc = series_description["describe_counts"].value_counts
    index_values = vc.index.values

    # FIXME: can be performance optimized by using weights in std, var, kurt and skew...

    return {
        "mean": np.average(index_values, weights=vc.values),
        "std": np.std(present_values, ddof=1),
        "variance": np.var(present_values, ddof=1),
        "min": np.min(index_values),
        "max": np.max(index_values),
        # Unbiased kurtosis obtained using Fisher's definition (kurtosis of normal == 0.0). Normalized by N-1.
        "kurtosis": series.kurt(),
        # Unbiased skew normalized by N-1
        "skewness": series.skew(),
        "sum": np.dot(index_values, vc.values),
    }


@describe_numeric_1d.register
@series_hashable
@series_handle_nulls
def pandas_describe_numeric_1d(
    config: Settings, series: pd.Series, summary: dict
) -> Tuple[Settings, pd.Series, NumericColumnResult]:
    """Describe a numeric series.

    Args:
        config: report Settings object
        series: The Series to describe.
        summary: The dict containing the series description so far.

    Returns:
        A dict containing calculated series description values.
    """

    result = NumericColumnResult()

    chi_squared_threshold = config.vars.num.chi_squared_threshold
    quantiles = config.vars.num.quantiles

    value_counts = summary["describe_counts"].value_counts

    negative_index = value_counts.index < 0
    result.n_negative = value_counts.loc[negative_index].sum()
    result.p_negative = result.n_negative / summary["describe_generic"].n

    infinity_values = [np.inf, -np.inf]
    infinity_index = value_counts.index.isin(infinity_values)
    result.n_infinite = value_counts.loc[infinity_index].sum()

    summary["n_zeros"] = 0
    if 0 in value_counts.index:
        summary["n_zeros"] = value_counts.loc[0]

    stats = summary

    if isinstance(series.dtype, _IntegerDtype):
        stats = numeric_stats_pandas(series)
        present_values = series.astype(str(series.dtype).lower())
        finite_values = present_values
    else:
        present_values = series.values
        finite_values = present_values[np.isfinite(present_values)]
        stats = numeric_stats_numpy(present_values, series, summary)
    result.min = stats["min"]
    result.max = stats["max"]
    result.mean = stats["mean"]
    result.std = stats["std"]
    result.variance = stats["variance"]
    result.skewness = stats["skewness"]
    result.kurtosis = stats["kurtosis"]
    result.sum = stats["sum"]

    result.mad = mad(present_values)

    if chi_squared_threshold > 0.0:
        result.chi_squared = chi_square(finite_values)

    result.range = result.max - result.min
    result.quantiles = {
        f"{percentile:.0%}": value
        for percentile, value in series.quantile(quantiles).to_dict().items()
    }

    result.iqr = result.quantiles["75%"] - result.quantiles["25%"]
    result.cv = result.std / result.mean if result.mean else np.NaN
    result.p_zeros = result.n_zeros / summary["describe_generic"].n
    result.p_infinite = result.n_infinite / summary["describe_generic"].n

    if series.is_monotonic_increasing:
        if series.is_unique:
            result.monotonic = Monotonicity.INCREASING_STRICT
        else:
            result.monotonic = Monotonicity.INCREASING
    elif series.is_monotonic_decreasing:
        if series.is_unique:
            result.monotonic = Monotonicity.DECREASING_STRICT
        else:
            result.monotonic = Monotonicity.DECREASING
    else:
        result.monotonic = Monotonicity.NOT_MONOTONIC

    r = histogram_compute(
        config,
        value_counts[~infinity_index].index.values,
        summary["describe_supported"].n_distinct,
        weights=value_counts[~infinity_index].values,
    )
    result.histogram = r["histogram"]

    return config, series, result
