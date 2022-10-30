import functools
from typing import Callable

import numpy as np
import pandas as pd
from pandas.api import types as pdt
from visions.backends.pandas.series_utils import series_handle_nulls

from pandas_profiling.config import Settings


def is_nullable(series: pd.Series, state: dict) -> bool:
    return series.count() > 0


def try_func(fn: Callable) -> Callable:
    @functools.wraps(fn)
    def inner(series: pd.Series, *args, **kwargs) -> bool:
        try:
            return fn(series, *args, **kwargs)
        except:  # noqa: E722
            return False

    return inner


def string_is_bool(series: pd.Series, state: dict, k: Settings) -> bool:
    @series_handle_nulls
    @try_func
    def tester(s: pd.Series, state: dict) -> bool:
        return s.str.lower().isin(k.keys()).all()

    if pdt.is_categorical_dtype(series):
        return False

    return tester(series, state)


def string_to_bool(series: pd.Series, state: dict, k: Settings) -> pd.Series:
    return series.str.lower().map(k)


def numeric_is_category(series: pd.Series, state: dict, k: Settings) -> bool:
    n_unique = series.nunique()
    threshold = k.vars.num.low_categorical_threshold
    return 1 <= n_unique <= threshold


def to_category(series: pd.Series, state: dict) -> pd.Series:
    hasnans = series.hasnans
    val = series.astype(str)
    if hasnans:
        val = val.replace("nan", np.nan)

    if int(pd.__version__.split(".")[0]) >= 1:
        val = val.astype("string")
    return val


@series_handle_nulls
def series_is_string(series: pd.Series, state: dict) -> bool:
    if not all(isinstance(v, str) for v in series.values[0:5]):
        return False
    try:
        return (series.astype(str).values == series.values).all()
    except (TypeError, ValueError):
        return False


@series_handle_nulls
def category_is_numeric(series: pd.Series, state: dict, k: Settings) -> bool:
    if pdt.is_bool_dtype(series) or object_is_bool(series, state):
        return False

    try:
        _ = series.astype(float)
        r = pd.to_numeric(series, errors="coerce")
        if r.hasnans and r.count() == 0:
            return False
    except:  # noqa: E722
        return False

    return not numeric_is_category(series, state, k)


def category_to_numeric(series: pd.Series, state: dict) -> pd.Series:
    return pd.to_numeric(series, errors="coerce")


hasnan_bool_name = "boolean" if int(pd.__version__.split(".")[0]) >= 1 else "Bool"


def to_bool(series: pd.Series) -> pd.Series:
    dtype = hasnan_bool_name if series.hasnans else bool
    return series.astype(dtype)


@series_handle_nulls
def object_is_bool(series: pd.Series, state: dict) -> bool:
    if pdt.is_object_dtype(series):
        bool_set = {True, False}
        try:
            ret = all(item in bool_set for item in series)
        except:  # noqa: E722
            ret = False

        return ret
    return False
