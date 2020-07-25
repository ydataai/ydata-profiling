import imghdr
from typing import Sequence
import os
import numpy as np
import pandas as pd

import imghdr
from urllib.parse import ParseResult, urlparse

from pandas_profiling.config import config
from pandas.api import types as pdt

import visions as vis

from visions.typesets.typeset import VisionsTypeset
from visions.types import VisionsBaseType
from visions.relations import IdentityRelation, InferenceRelation, TypeRelation
from visions.utils.series_utils import nullable_series_contains
<<<<<<< HEAD
=======

>>>>>>> 2c6b5df5f37940035b9cb22b5338f61e612147a4

# TODO: Hack
Generic = vis.Generic

<<<<<<< HEAD
# TODO: This may not be a good idea with it's global context
def named_series_cache():
    cache = {}
    def inner(series):
        if series.name is None:
            return series.nunique()

        if series.name not in cache:
            cache[series.name] = series.nunique()
        return cache[series.name]
    return inner

nunique_cache = named_series_cache()

=======
# attribute mixin
>>>>>>> 2c6b5df5f37940035b9cb22b5338f61e612147a4
class ProfilingTypeCategories:
    continuous = False
    categorical = False


<<<<<<< HEAD
class PandasProfilingBaseType(VisionsBaseType, ProfilingTypeCategories):
    pass


def numeric_is_category(series):
    n_unique = nunique_cache(series)
    return  n_unique <= config["vars"]["num"]["low_categorical_threshold"].get(int)


class Category(PandasProfilingBaseType):
=======
class Category(VisionsBaseType, ProfilingTypeCategories):
>>>>>>> 2c6b5df5f37940035b9cb22b5338f61e612147a4
    """**Category** implementation of :class:`visions.types.VisionsBaseType`.

    Examples:
    """
    categorical = True

    @classmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
<<<<<<< HEAD
        return [IdentityRelation(cls, vis.Object),
                IdentityRelation(cls, vis.Generic),
                InferenceRelation(cls, Numeric, relationship=numeric_is_category, transformer=lambda s: s.astype(str))]

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        # is_string_dtype returns True for Sequences of Union[Boolean, Missing]
        if pdt.is_categorical_dtype(series):
=======
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
>>>>>>> 2c6b5df5f37940035b9cb22b5338f61e612147a4
            return True
        elif pdt.is_string_dtype(series):
            return False if any(v in {True, False} for v in series) else True

        if series.hasnans:
            series = series.dropna()
            if series.empty:
                return False
        return all(isinstance(v, str) for v in series)


<<<<<<< HEAD
def string_is_path(series) -> bool:
    return all(os.path.isabs(p) for p in series.dropna())


def to_path(series: pd.Series) -> pd.Series:
    return series.apply(pathlib.PurePath)


class Path(PandasProfilingBaseType):
    categorical = True
    @classmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        relations = [IdentityRelation(cls, Category),
=======
class Path(VisionsBaseType, ProfilingTypeCategories):
    categorical = True
    @classmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        relations = [
            IdentityRelation(cls, Category),
>>>>>>> 2c6b5df5f37940035b9cb22b5338f61e612147a4
        ]
        return relations

    @classmethod
    @nullable_series_contains
    def contains_op(cls, series: pd.Series) -> bool:
<<<<<<< HEAD
        try:
            return all(os.path.isabs(p) for p in result)
        except:
            return False
=======
        return all(os.path.isabs(p) for p in series)

>>>>>>> 2c6b5df5f37940035b9cb22b5338f61e612147a4

class File(PandasProfilingBaseType):
    categorical = True
    @classmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        return [IdentityRelation(cls, Path)]

<<<<<<< HEAD
    @classmethod
    @nullable_series_contains
    def contains_op(cls, series: pd.Series) -> bool:
        try:
            return all(os.path.exists(p) for p in result)
        except:
            return False
=======
    @nullable_series_contains
    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        return all(os.path.exists(p) for p in series)

>>>>>>> 2c6b5df5f37940035b9cb22b5338f61e612147a4

class Image(PandasProfilingBaseType):
    categorical = True
    @classmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        return [IdentityRelation(cls, File)]

    @classmethod
    @nullable_series_contains
    def contains_op(cls, series: pd.Series) -> bool:
<<<<<<< HEAD
        try:
            return all(imghdr.what(p) for p in result)
        except (TypeError, ValueError):
            return False


def test_url(series) -> bool:
    try:
        url_gen = (urlparse(x) for x in series)
        return all(x.netloc and x.scheme for x in url_gen)
    except AttributeError:
        return False


def to_url(series: pd.Series) -> pd.Series:
    return series.apply(urlparse)


class URL(PandasProfilingBaseType):
    categorical = True
    @classmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        return [IdentityRelation(cls, Category, relationship=test_url, transformer=to_url),]
=======
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
>>>>>>> 2c6b5df5f37940035b9cb22b5338f61e612147a4

    @classmethod
    @nullable_series_contains
    def contains_op(cls, series: pd.Series) -> bool:
        return test_url(series)

<<<<<<< HEAD

def is_date(series):
    try:
        _ = pd.to_datetime(series)
        return True
    except:
        return False
=======
# def is_complex_str(series) -> bool:
#     try:
#         complex_gen = (np.complex(x) for x in series)
#         return any(x.imag != 0 for x in complex_gen)
#     except:
#         return False
>>>>>>> 2c6b5df5f37940035b9cb22b5338f61e612147a4


class Date(PandasProfilingBaseType):
    categorical = True
    @classmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        return [
            IdentityRelation(cls, vis.Generic),
<<<<<<< HEAD
            InferenceRelation(cls, Category, relationship=is_date, transformer=pd.to_datetime,),
        ]
    
    @classmethod
    @nullable_series_contains
    def contains_op(cls, series: pd.Series) -> bool:
        return pd.api.types.is_datetime64_dtype(series)


def string_is_numeric(series):
    try:
        _ = pd.to_numeric(series)
        if nunique_cache(series) > config["vars"]["num"]["low_categorical_threshold"].get(int):
            return False
    except:
        return False
    return True
=======
            # InferenceRelation(cls, Category, relationship=is_complex_str, transformer=lambda x: x),
        ]

# def is_date(series):
#     try:
#         _ = pd.to_datetime(series)
#         return True
#     except:
#         return False
>>>>>>> 2c6b5df5f37940035b9cb22b5338f61e612147a4


class Numeric(PandasProfilingBaseType):
    continuous = True
    @classmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
<<<<<<< HEAD
        return [IdentityRelation(cls, vis.Generic),
                InferenceRelation(cls, Category, relationship=string_is_numeric, transformer=pd.to_numeric,)]

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        return pdt.is_numeric_dtype(series) and not pdt.is_bool(series)
=======
        return [
            IdentityRelation(cls, vis.Generic),
            # InferenceRelation(cls, Category, relationship=is_date, transformer=lambda x: pd.to_datetime(x)),
        ]
>>>>>>> 2c6b5df5f37940035b9cb22b5338f61e612147a4


def test_string_is_complex(series) -> bool:
    try:
        complex_gen = (np.complex(x) for x in series)
        return any(x.imag != 0 for x in complex_gen)
    except:
        return False


class Complex(PandasProfilingBaseType):
    continuous = True
    @classmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        return [
            IdentityRelation(cls, Numeric),
            InferenceRelation(cls, Category, relationship=test_string_is_complex, transformer=lambda x: x.apply(np.complex)
        ),
    ]

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        return pdt.is_complex_dtype(series)


PP_bool_map = [{'yes': True, 'no': False},
        {'y': True, 'n': False},
        {'true': True, 'false': False},
        {'t': True, 'f': False}]


def string_is_bool(series):
    bool_map_keys = [k for d in PP_bool_map for k, v in d.items()]
    return series.str.lower().isin(bool_map_keys + [None]).all()


def string_to_bool(series):
    return series.str.lower().map(PP_bool_map)


class Bool(PandasProfilingBaseType):
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
            InferenceRelation(cls, 
                              vis.Object, 
                              relationship=lambda s: s.isin({True, False, np.nan, None}).all(),
                              transformer=lambda s: s.astype("Bool")),
            InferenceRelation(
                cls,
                Numeric,
                relationship=lambda s: s.isin({0, 1, 0.0, 1.0, np.nan, None}).all(),
                transformer=lambda s: s,
            ),
        ]

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        return not pdt.is_categorical_dtype(series) and pdt.is_bool_dtype(series)


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
