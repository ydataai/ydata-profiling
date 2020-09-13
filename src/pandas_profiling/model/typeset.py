import imghdr
import os
import functools
from typing import Sequence, Callable
from urllib.parse import urlparse

import numpy as np
import pandas as pd
import visions as vis
from pandas.api import types as pdt
from visions.relations import IdentityRelation, InferenceRelation, TypeRelation
from visions.types import VisionsBaseType
from visions.typesets.typeset import VisionsTypeset
from visions.utils.series_utils import (
    func_nullable_series_contains,
    nullable_series_contains,
)

from pandas_profiling.config import config


class ProfilingTypeCategories:
    continuous = False
    categorical = False


class PandasProfilingBaseType(VisionsBaseType, ProfilingTypeCategories):
    pass


class Unsupported(vis.Generic, ProfilingTypeCategories):
    pass


def applied_to_nonnull(fn: Callable) -> Callable:
    @functools.wraps(fn)
    def inner(series: pd.Series) -> pd.Series:
        if series.hasnans:
            new_series = series.copy()
            notna = series.notna()
            new_series[notna] = fn(series[notna])
            return new_series
        return fn(series)

    return inner


def try_func(fn: Callable) -> Callable:
    @functools.wraps(fn)
    def inner(series: pd.Series) -> bool:
        try:
            return fn(series)
        except:
            return False

    return inner


def numeric_is_category(series: pd.Series) -> bool:
    n_unique = series.nunique()
    return n_unique < config["vars"]["num"]["low_categorical_threshold"].get(int)


@func_nullable_series_contains
def series_is_string(series: pd.Series) -> bool:
    return all(isinstance(v, str) for v in series)


class Category(PandasProfilingBaseType):
    """**Category** implementation of :class:`visions.types.VisionsBaseType`.

    Examples:
    """

    categorical = True

    @classmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        return [
            IdentityRelation(cls, Unsupported),
            InferenceRelation(
                cls,
                Numeric,
                relationship=numeric_is_category,
                transformer=applied_to_nonnull(lambda s: s.astype(str)),
            ),
        ]

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        if pdt.is_categorical_dtype(series) and not pdt.is_bool_dtype(series):
            return True
        return series_is_string(series)


class Path(PandasProfilingBaseType):
    categorical = True

    @classmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        relations = [
            IdentityRelation(cls, Category),
        ]
        return relations

    @classmethod
    @nullable_series_contains
    def contains_op(cls, series: pd.Series) -> bool:
        return all(os.path.isabs(p) for p in series)


class File(PandasProfilingBaseType):
    categorical = True

    @classmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        return [IdentityRelation(cls, Path)]

    @classmethod
    @nullable_series_contains
    def contains_op(cls, series: pd.Series) -> bool:
        return all(os.path.exists(p) for p in series)


class Image(PandasProfilingBaseType):
    categorical = True

    @classmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        return [IdentityRelation(cls, File)]

    @classmethod
    @nullable_series_contains
    def contains_op(cls, series: pd.Series) -> bool:
        return all(imghdr.what(p) for p in series)


class URL(PandasProfilingBaseType):
    categorical = True

    @classmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        return [IdentityRelation(cls, Category)]

    @classmethod
    @nullable_series_contains
    def contains_op(cls, series: pd.Series) -> bool:
        try:
            url_gen = (urlparse(x) for x in series)
            return all(x.netloc and x.scheme for x in url_gen)
        except AttributeError:
            return False


@try_func
def is_date(series: pd.Series) -> bool:
    _ = pd.to_datetime(series)
    return True


class Date(PandasProfilingBaseType):
    categorical = True

    @classmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        return [
            IdentityRelation(cls, Unsupported),
            # InferenceRelation(cls, Category, relationship=is_date, transformer=pd.to_datetime,),
        ]

    @classmethod
    @nullable_series_contains
    def contains_op(cls, series: pd.Series) -> bool:
        return pd.api.types.is_datetime64_dtype(series)


@try_func
def category_is_numeric(series):
    if pdt.is_categorical_dtype(series):
        return False
    return not numeric_is_category(pd.to_numeric(series))


class Numeric(PandasProfilingBaseType):
    continuous = True

    @classmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        return [
            IdentityRelation(cls, Unsupported),
            # InferenceRelation(
            #    cls,
            #    Category,
            #    relationship=category_is_numeric,
            #    transformer=pd.to_numeric,
            # ),
        ]

    @classmethod
    @nullable_series_contains
    def contains_op(cls, series: pd.Series) -> bool:
        return not pdt.is_bool_dtype(series) and pdt.is_numeric_dtype(series)


@try_func
def string_is_complex(series) -> bool:
    complex_gen = (np.complex(x) for x in series)
    return any(x.imag != 0 for x in complex_gen)


class Complex(PandasProfilingBaseType):
    continuous = True

    @classmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        return [
            IdentityRelation(cls, Numeric),
            # InferenceRelation(cls, Category, relationship=string_is_complex, transformer=lambda x: x.apply(np.complex)
            # ),
        ]

    @classmethod
    @nullable_series_contains
    def contains_op(cls, series: pd.Series) -> bool:
        return pdt.is_complex_dtype(series)


PP_bool_map = {
    "yes": True,
    "no": False,
    "y": True,
    "n": False,
    "true": True,
    "false": False,
    "t": True,
    "f": False,
    "1": True,
    "0": False,
    "1.0": True,
    "0.0": False,
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
def string_to_bool(series: pd.Series) -> pd.Series:
    return series.str.lower().map(PP_bool_map)


def to_bool(series: pd.Series) -> pd.Series:
    if series.hasnans:
        return series.astype("Bool")
    else:
        return series.astype(bool)


class Bool(PandasProfilingBaseType):
    categorical = True

    @classmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        return [
            IdentityRelation(cls, Unsupported),
            InferenceRelation(
                cls,
                Category,
                relationship=string_is_bool,
                transformer=string_to_bool,
            ),
            InferenceRelation(
                cls,
                Numeric,
                relationship=try_func(
                    lambda s: s.isin({0, 1, 0.0, 1.0, np.nan, None}).all()
                ),
                transformer=to_bool,
            ),
        ]

    @classmethod
    @nullable_series_contains
    def contains_op(cls, series: pd.Series) -> bool:
        if pdt.is_object_dtype(series):
            return try_func(lambda s: s.isin({True, False}).all())(series)

        return pdt.is_bool_dtype(series) and not pdt.is_categorical_dtype(series)


class ProfilingTypeSet(VisionsTypeset):
    """Base typeset for pandas-profiling"""

    def __init__(self):
        types = {
            Unsupported,
            Bool,
            Numeric,
            Date,
            Complex,
            Category,
        }

        if config["vars"]["path"]["active"].get(bool):
            types.add(Path)
            if config["vars"]["file"]["active"].get(bool):
                types.add(File)
                if config["vars"]["image"]["active"].get(bool):
                    types.add(Image)
                else:
                    raise ValueError(
                        "Image type only supported when File and Path type are also active"
                    )
            else:
                raise ValueError("File type only supported when Path type is active")
        if config["vars"]["url"]["active"].get(bool):
            types.add(URL)

        super().__init__(types)


if __name__ == "__main__":
    from matplotlib import pyplot as plt

    config.set_arg_group("explorative")
    ts = ProfilingTypeSet()
    ts.plot_graph()
    plt.show()
