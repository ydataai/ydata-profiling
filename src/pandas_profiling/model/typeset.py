from typing import Sequence
import os
import numpy as np
import pandas as pd
import pathlib 

from urllib.parse import ParseResult, urlparse

from pandas_profiling.config import config
from pandas.api import types as pdt

import visions as vis

from visions.typesets.typeset import VisionsTypeset
from visions.types import VisionsBaseType
from visions.relations import IdentityRelation, InferenceRelation, TypeRelation
from visions.utils.series_utils import nullable_series_contains


# TODO: Hack
Generic = vis.Generic

# attribute mixin
class ProfilingTypeCategories:
    continuous = False
    categorical = False


class Object(VisionsBaseType):
    """**Object** implementation of :class:`visions.types.type.VisionsBaseType`.

    Examples:
        >>> x = pd.Series(['a', 1, np.nan])
        >>> x in visions.Object
        True
    """

    @classmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        return [IdentityRelation(cls, Generic)]

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        return pdt.is_object_dtype(series) or pdt.is_categorical_dtype(series)


class Category(VisionsBaseType, ProfilingTypeCategories):
    """**Category** implementation of :class:`visions.types.VisionsBaseType`.

    Examples:
    """
    categorical = True

    @classmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        return [IdentityRelation(cls, Object)]

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        is_valid_dtype = pdt.is_categorical_dtype(series) # or pdt.is_string_dtype(series)
        if is_valid_dtype:
            return True

        if series.hasnans:
            series = series.dropna()
            if series.empty:
                return False
        return all(isinstance(v, str) for v in series)


def string_is_path(series) -> bool:
    return all(os.path.isabs(p) for p in series.dropna())


def to_path(series: pd.Series) -> pd.Series:
    return series.apply(pathlib.PurePath)


class Path(vis.Path, ProfilingTypeCategories):
    categorical = True
    @classmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        relations = [
            IdentityRelation(cls, Object),
            InferenceRelation(
                cls, Category, relationship=string_is_path, transformer=to_path
            ),
        ]
        return relations


class File(vis.File, ProfilingTypeCategories):
    categorical = True
    @classmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        return [IdentityRelation(cls, Path)]


class Image(vis.Image, ProfilingTypeCategories):
    categorical = True
    @classmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        return [IdentityRelation(cls, File)]


def test_url(series) -> bool:
    try:
        url_gen = (urlparse(x) for x in series)
        return all(x.netloc and x.scheme for x in url_gen)
    except AttributeError:
        return False


def to_url(series: pd.Series) -> pd.Series:
    return series.apply(urlparse)


class URL(VisionsBaseType, ProfilingTypeCategories):
    categorical = True
    @classmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        return [IdentityRelation(cls, Category)]

    @classmethod
    @nullable_series_contains
    def contains_op(cls, series: pd.Series) -> bool:
        return all(
            isinstance(y, ParseResult) and all((y.netloc, y.scheme)) for x in series for y in [urlparse(x)]
        )


def test_string_is_complex(series) -> bool:
    try:
        complex_gen = (np.complex(x) for x in series)
        return any(x.imag != 0 for x in complex_gen)
    except:
        return False


class Complex(vis.Complex, ProfilingTypeCategories):
    continuous = True
    @classmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        return [
            IdentityRelation(cls, vis.Generic),
            InferenceRelation(cls, Category, relationship=test_string_is_complex, transformer=lambda x: x.apply(np.complex)
        ),
    ]

def is_date(series):
    try:
        _ = pd.to_datetime(series)
        return True
    except:
        return False


class Date(vis.DateTime, ProfilingTypeCategories):
    categorical = True
    @classmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        return [
            IdentityRelation(cls, vis.Generic),
            InferenceRelation(cls, Category, relationship=is_date, transformer=pd.to_datetime,),
        ]


class Numeric(vis.VisionsBaseType, ProfilingTypeCategories):
    continuous = True
    @classmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        return [IdentityRelation(cls, vis.Generic)]

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        return pdt.is_float_dtype(series) or pdt.is_integer_dtype(series)


PP_bool_map = [{'yes': True, 'no': False},
        {'y': True, 'n': False},
        {'true': True, 'false': False},
        {'t': True, 'f': False}]

def string_is_bool(series):
    bool_map_keys = [k for d in PP_bool_map for k, v in d.items()]
    return series.str.lower().isin(bool_map_keys + [None]).all()


def string_to_bool(series):
    return series.str.lower().map(PP_bool_map)


class Bool(vis.Boolean, ProfilingTypeCategories):
    categorical = True
    @classmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        return [
            IdentityRelation(cls, vis.Generic),
            InferenceRelation(
                cls,
                Category,
                relationship=string_is_bool,
                transformer=string_to_bool
            ),
            InferenceRelation(
                cls,
                Numeric,
                relationship=lambda s: s.isin({0, 1, 0.0, 1.0, np.nan, None}).all(),
                transformer=lambda s: s.astype("Bool"),
            ),
        ]


class ProfilingTypeSet(VisionsTypeset):
    """Base typeset for pandas-profiling"""
    def __init__(self):
        types = {
            Bool,
            Numeric,
            Date,
            Complex,
            Object,
            Category,
        }

        if config["vars"]["path"]["active"].get(bool):
            types.add(Path)
        if config["vars"]["file"]["active"].get(bool):
            types.add(File)
        if config["vars"]["image"]["active"].get(bool):
            types.add(Image)
        if config["vars"]["url"]["active"].get(bool):
            types.add(URL)

        super().__init__(types)