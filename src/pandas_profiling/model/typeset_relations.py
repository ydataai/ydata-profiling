import functools

import pandas as pd
from pandas.api import types as pdt
from visions.utils import func_nullable_series_contains

from pandas_profiling.config import config


def applied_to_nonnull(fn):
    @functools.wraps(fn)
    def inner(series):
        if series.hasnans:
            new_series = series.copy()
            notna = series.notna()
            new_series[notna] = fn(series[notna])
            return new_series
        return fn(series)

    return inner


def try_func(fn):
    @functools.wraps(fn)
    def inner(series: pd.Series) -> bool:
        try:
            return fn(series)
        except:
            return False

    return inner


def string_test_maker():
    bool_map_keys = list(PP_bool_map.keys())

    @func_nullable_series_contains
    def inner(series):
        if pdt.is_categorical_dtype(series):
            return False

        try:
            return series.str.lower().isin(bool_map_keys).all()
        except:
            return False

    return inner


PP_bool_map = {
    "yes": True,
    "no": False,
    "y": True,
    "n": False,
    "true": True,
    "false": False,
    "t": True,
    "f": False,
}


string_is_bool = string_test_maker()


@applied_to_nonnull
def string_to_bool(series):
    return series.str.lower().map(PP_bool_map)


def to_bool(series: pd.Series) -> pd.Series:
    if series.hasnans:
        return series.astype("Bool")
    else:
        return series.astype(bool)


def numeric_is_category(series):
    n_unique = series.nunique()
    threshold = config["vars"]["num"]["low_categorical_threshold"].get(int)
    return 1 <= n_unique <= threshold


def category_is_numeric(series):
    if pdt.is_bool_dtype(series):
        return False

    try:
        r = pd.to_numeric(series, errors='coerce')
        if r.hasnans and r.count() == 0:
            return False
    except:
        return False

    n_unique = series.nunique()
    threshold = config["vars"]["num"]["low_categorical_threshold"].get(int)
    if 1 <= n_unique <= threshold:
        return False
    return True


def category_to_numeric(series):
    return pd.to_numeric(series, errors="coerce")
