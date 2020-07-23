import imghdr
from typing import Sequence
import os
import numpy as np
import pandas as pd

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


class Category(VisionsBaseType, ProfilingTypeCategories):
    """**Category** implementation of :class:`visions.types.VisionsBaseType`.

    Examples:
    """
    categorical = True

    @classmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        return [
            IdentityRelation(cls, Generic),
            InferenceRelation(
                cls,
                Numeric,
                relationship=lambda s: s.nunique() < config["vars"]["num"]["low_categorical_threshold"].get(int),
                transformer=lambda s: s.astype(str)
            )
        ]

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


class Path(VisionsBaseType, ProfilingTypeCategories):
    categorical = True
    @classmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        relations = [
            IdentityRelation(cls, Category),
        ]
        return relations

    @nullable_series_contains
    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        return all(os.path.isabs(p) for p in series)


class File(vis.File, ProfilingTypeCategories):
    categorical = True
    @classmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        return [IdentityRelation(cls, Path)]

    @nullable_series_contains
    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        return all(os.path.exists(p) for p in series)


class Image(vis.Image, ProfilingTypeCategories):
    categorical = True
    @classmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        return [IdentityRelation(cls, File)]

    @classmethod
    @nullable_series_contains
    def contains_op(cls, series: pd.Series) -> bool:
        return all(
            imghdr.what(p) for p in series
        )


class URL(VisionsBaseType, ProfilingTypeCategories):
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


# def is_complex_str(series) -> bool:
#     try:
#         complex_gen = (np.complex(x) for x in series)
#         return any(x.imag != 0 for x in complex_gen)
#     except:
#         return False


class Complex(vis.Complex, ProfilingTypeCategories):
    continuous = True
    @classmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        return [
            IdentityRelation(cls, vis.Generic),
            # InferenceRelation(cls, Category, relationship=is_complex_str, transformer=lambda x: x),
        ]

# def is_date(series):
#     try:
#         _ = pd.to_datetime(series)
#         return True
#     except:
#         return False


class Date(vis.DateTime, ProfilingTypeCategories):
    categorical = True
    @classmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        return [
            IdentityRelation(cls, vis.Generic),
            # InferenceRelation(cls, Category, relationship=is_date, transformer=lambda x: pd.to_datetime(x)),
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
                transformer=lambda s: s
            ),
            InferenceRelation(
                cls,
                Numeric,
                relationship=lambda s: s.isin({0, 1, 0.0, 1.0, np.nan, None}).all(),
                transformer=lambda s: s,
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
            Category,
        }

        if config["vars"]["path"]["active"].get(bool):
            types.add(Path)
            if config["vars"]["file"]["active"].get(bool):
                types.add(File)
                if config["vars"]["image"]["active"].get(bool):
                    types.add(Image)
                else:
                    raise ValueError("Image type only supported when File and Path type are also active")
            else:
                raise ValueError("File type only supported when Path type is active")
        if config["vars"]["url"]["active"].get(bool):
            types.add(URL)

        super().__init__(types)


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    config.set_arg_group("explorative")
    ts = ProfilingTypeSet()
    ts.plot_graph()
    plt.show()
