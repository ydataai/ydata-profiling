import functools
from typing import Any, Callable, Optional, Tuple, TypeVar

import numpy as np
import pandas as pd
from multimethod import multimethod
from scipy.stats.stats import chisquare

from pandas_profiling.config import Settings
from pandas_profiling.model.schema import (
    BooleanColumnResult,
    CategoricalColumnResult,
    CountColumnResult,
    DateColumnResult,
    FileColumnResult,
    GenericColumnResult,
    ImageColumnResult,
    NumericColumnResult,
    PathColumnResult,
    SupportedColumnResult,
    UrlColumnResult,
)

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


def histogram_spark_compute(
    config: Settings,
    df,
    minim,
    maxim,
    n_unique
) -> dict:
    import pyspark.sql.functions as F
    df = df.na.drop()
    bins = config.plot.histogram.bins
    bins = 10 if bins == 0 else min(bins, n_unique)

    bin_width = (maxim - minim) / float(bins)
    left_list = [minim + i * bin_width for i in range(bins)]

    bin_id = 0
    condition = F
    for left in left_list[:-1]:
        right = left + bin_width
        condition = condition.when(F.col(df.columns[0]) < right, bin_id)
        bin_id += 1
    condition = condition.otherwise(bin_id)

    bin_data = (df
                .withColumn("bin_id", condition)
                .groupBy("bin_id").count()
                ).toPandas()

    # If no data goes into one bin, it won't
    # appear in bin_data; so we should fill
    # in the blanks
    bin_data.index = bin_data["bin_id"]
    new_index = list(range(bins))
    bin_data = bin_data.reindex(new_index)
    bin_data = bin_data.drop("bin_id", axis=1).fillna(0)

    bin_data.index = left_list

    return bin_data.squeeze(), bins


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
        if not summary["describe_counts"].hashable:
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
) -> Tuple[Settings, Any, CountColumnResult]:
    raise NotImplementedError()


@multimethod
def describe_supported(
    config: Settings, series: Any, summary: dict
) -> Tuple[Settings, Any, SupportedColumnResult]:
    raise NotImplementedError()


@multimethod
def describe_generic(
    config: Settings, series: Any, summary: dict
) -> Tuple[Settings, Any, GenericColumnResult]:
    raise NotImplementedError()


@multimethod
def describe_numeric_1d(
    config: Settings, series: Any, summary: dict
) -> Tuple[Settings, Any, NumericColumnResult]:
    raise NotImplementedError()


@multimethod
def describe_date_1d(
    config: Settings, series: Any, summary: dict
) -> Tuple[Settings, Any, DateColumnResult]:
    raise NotImplementedError()


@multimethod
def describe_categorical_1d(
    config: Settings, series: Any, summary: dict
) -> Tuple[Settings, Any, CategoricalColumnResult]:
    raise NotImplementedError()


@multimethod
def describe_url_1d(
    config: Settings, series: Any, summary: dict
) -> Tuple[Settings, Any, UrlColumnResult]:
    raise NotImplementedError()


@multimethod
def describe_file_1d(
    config: Settings, series: Any, summary: dict
) -> Tuple[Settings, Any, FileColumnResult]:
    raise NotImplementedError()


@multimethod
def describe_path_1d(
    config: Settings, series: Any, summary: dict
) -> Tuple[Settings, Any, PathColumnResult]:
    raise NotImplementedError()


@multimethod
def describe_image_1d(
    config: Settings, series: Any, summary: dict
) -> Tuple[Settings, Any, ImageColumnResult]:
    raise NotImplementedError()


@multimethod
def describe_boolean_1d(
    config: Settings, series: Any, summary: dict
) -> Tuple[Settings, Any, BooleanColumnResult]:
    raise NotImplementedError()
