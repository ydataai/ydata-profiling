import functools
from typing import Any, Callable, Optional, Tuple, TypeVar, Union

import numpy as np
import pandas as pd
from multimethod import multimethod
from scipy.stats import chisquare

from ydata_profiling.config import Settings

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

def safe_histogram(
    values: np.ndarray,
    bins: Union[int, str, np.ndarray] = "auto",
    weights: Optional[np.ndarray] = None,
    density: bool = False,
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Wrapper to avoid
    ValueError: Too many bins for data range. Cannot create N finite-sized bins.
    """
    try:
        return np.histogram(values, bins=bins, weights=weights, density=density)
    except ValueError as exc:
        if "Too many bins for data range" in str(exc):
            try:
                return np.histogram(values, bins="auto", weights=weights, density=density)
            except ValueError:
                finite = values[np.isfinite(values)]
                if finite.size == 0:
                    return np.array([]), np.array([])
                vmin = float(np.min(finite))
                vmax = float(np.max(finite))
                if vmin == vmax:
                    eps = 0.5 if vmin == 0 else abs(vmin) * 0.5
                    bin_edges = np.array([vmin - eps, vmin + eps])
                else:
                    bin_edges = np.array([vmin, vmax])
                return np.histogram(values, bins=bin_edges, weights=weights, density=density)
        raise

def histogram_compute(
    config: Settings,
    finite_values: np.ndarray,
    n_unique: int,
    name: str = "histogram",
    weights: Optional[np.ndarray] = None,
) -> dict:
    stats = {}
    if len(finite_values) == 0:
        return {name: []}

    hist_config = config.plot.histogram

    # Compute data range
    finite = finite_values[np.isfinite(finite_values)]
    vmin = float(np.min(finite))
    vmax = float(np.max(finite))
    data_range = vmax - vmin

    # Choose of Bins based on observed data values
    if data_range == 0:
        eps = 0.5 if vmin == 0 else abs(vmin) * 0.1
        bins = np.array([vmin - eps, vmin + eps])
    else:
        requested_bins = hist_config.bins if hist_config.bins > 0 else "auto"

        if isinstance(requested_bins, int):
            safe_bins = min(requested_bins, n_unique, hist_config.max_bins)

            safe_bins = max(1, safe_bins)

            bins = np.linspace(vmin, vmax, safe_bins + 1)
        else:
            bins = np.histogram_bin_edges(finite_values, bins="auto")
            if len(bins) - 1 > hist_config.max_bins:
                bins = np.linspace(vmin, vmax, hist_config.max_bins + 1)

    hist = np.histogram(
        finite_values,
        bins=bins,
        weights=weights,
        density=hist_config.density,
    )

    stats[name] = hist
    return stats



def chi_square(
    values: Optional[np.ndarray] = None, histogram: Optional[np.ndarray] = None
) -> dict:
    if histogram is None:
        bins = np.histogram_bin_edges(values, bins="auto")
        histogram, _ = np.histogram(values, bins=bins)
    if len(histogram) == 0 or np.sum(histogram) == 0:
        return {"statistic": 0, "pvalue": 0}
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
def describe_text_1d(
    config: Settings, series: Any, summary: dict
) -> Tuple[Settings, Any, dict, Any]:
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


@multimethod
def describe_timeseries_1d(
    config: Settings, series: Any, summary: dict
) -> Tuple[Settings, Any, dict]:
    raise NotImplementedError()
