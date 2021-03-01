import functools
from typing import Any, Callable, Optional, Tuple, TypeVar

import numpy as np
import pandas as pd
from multimethod import multimethod
from scipy.stats.stats import chisquare

from pandas_profiling.config import Settings

T = TypeVar("T")


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


def chi_square(
    values: Optional[np.ndarray] = None, histogram: Optional[np.ndarray] = None
) -> dict:
    if histogram is None:
        histogram, _ = np.histogram(values, bins="auto")
    return dict(chisquare(histogram)._asdict())


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


@multimethod
def describe_url_1d(
    config: Settings, series: Any, summary: dict
) -> Tuple[Settings, Any, dict]:
    raise NotImplementedError()


@multimethod
def describe_file_1d(
    config: Settings, series: Any, summary: dict
) -> Tuple[Settings, Any, dict]:
    raise NotImplementedError()


@multimethod
def describe_path_1d(
    config: Settings, series: Any, summary: dict
) -> Tuple[Settings, Any, dict]:
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
