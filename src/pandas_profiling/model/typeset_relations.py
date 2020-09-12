import functools

import pandas as pd
from pandas.api import types as pdt
from visions.utils import func_nullable_series_contains

from pandas_profiling.config import config


def is_nullable(series) -> bool:
    return series.count() > 0


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


# TODO: config!
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


def string_is_bool(series) -> bool:
    @try_func
    @func_nullable_series_contains
    def tester(s: pd.Series) -> bool:
        return s.str.lower().isin(PP_bool_map.keys()).all()

    if pdt.is_categorical_dtype(series):
        return False

    return tester(series)


@applied_to_nonnull
def string_to_bool(series):
    return series.str.lower().map(PP_bool_map)


def numeric_is_category(series):
    n_unique = series.nunique()
    threshold = config["vars"]["num"]["low_categorical_threshold"].get(int)
    # TODO <= threshold OR < threshold?
    return 1 <= n_unique <= threshold


@applied_to_nonnull
def to_category(series):
    return series.astype(str)


@func_nullable_series_contains
def series_is_string(series: pd.Series) -> bool:
    return all(isinstance(v, str) for v in series)


def category_is_numeric(series):
    if pdt.is_bool_dtype(series) or object_is_bool(series):
        return False

    try:
        _ = series.astype(float)
        r = pd.to_numeric(series, errors="coerce")
        if r.hasnans and r.count() == 0:
            return False
    except:
        return False

    return not numeric_is_category(series)


def category_to_numeric(series):
    return pd.to_numeric(series, errors="coerce")


hasnan_bool_name = "boolean" if int(pd.__version__.split(".")[0]) >= 1 else "Bool"


def to_bool(series: pd.Series) -> pd.Series:
    dtype = hasnan_bool_name if series.hasnans else bool
    return series.astype(dtype)


@func_nullable_series_contains
def object_is_bool(series: pd.Series) -> bool:
    if pdt.is_object_dtype(series):
        bool_set = {True, False}
        # TODO: try func? is in?
        try:
            ret = all(item in bool_set for item in series)
        except:
            ret = False

        return ret
    return False
