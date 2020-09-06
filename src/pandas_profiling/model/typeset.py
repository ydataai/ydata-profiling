import imghdr
import os
from urllib.parse import urlparse

import pandas as pd
import visions
from pandas.api import types as pdt
from visions import VisionsBaseType, VisionsTypeset
from visions.relations import IdentityRelation, InferenceRelation

# from visions.types.url import test_url, to_url
from visions.utils import nullable_series_contains

from pandas_profiling.config import config

# class ProfilingTypeCategories:
#     continuous = False
#     categorical = False
from pandas_profiling.model.typeset_relations import (
    applied_to_nonnull,
    category_is_numeric,
    category_to_numeric,
    numeric_is_category,
    string_is_bool,
    string_to_bool,
)


class PandasProfilingBaseType(VisionsBaseType):
    pass


class Unsupported(visions.Generic):
    pass


class Numeric(PandasProfilingBaseType):
    @classmethod
    def get_relations(cls):
        return [
            IdentityRelation(cls, Unsupported),
            InferenceRelation(
                cls,
                Categorical,
                relationship=category_is_numeric,
                transformer=category_to_numeric,
            ),
        ]

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        dcheck = not pdt.is_bool_dtype(series) and pdt.is_numeric_dtype(series)
        if not dcheck:
            return False

        if series.hasnans and series.count() == 0:
            return False

        return True


class DateTime(PandasProfilingBaseType):
    @classmethod
    def get_relations(cls):
        return [
            IdentityRelation(cls, Unsupported),
            # InferenceRelation(cls, Categorical, relationship=is_date, transformer=pd.to_datetime,),
        ]

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        return pdt.is_datetime64_any_dtype(series)


class Categorical(PandasProfilingBaseType):
    @classmethod
    def get_relations(cls):
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
        is_valid_dtype = pdt.is_categorical_dtype(series) or pdt.is_bool_dtype(series)
        if is_valid_dtype:
            return True

        if series.hasnans:
            series = series.dropna()
            if series.empty:
                return False
        return all(isinstance(v, (str, bool)) for v in series)


class Boolean(PandasProfilingBaseType):
    @classmethod
    def get_relations(cls):
        return [
            IdentityRelation(cls, Categorical),
            InferenceRelation(
                cls,
                Categorical,
                relationship=string_is_bool,
                transformer=string_to_bool,
            ),
        ]

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        return pdt.is_bool_dtype(series)


class URL(PandasProfilingBaseType):
    @classmethod
    def get_relations(cls):
        relations = [
            IdentityRelation(cls, Categorical),
        ]
        return relations

    @classmethod
    @nullable_series_contains
    def contains_op(cls, series: pd.Series) -> bool:
        try:
            url_gen = (urlparse(x) for x in series)
            return all(x.netloc and x.scheme for x in url_gen)
        except AttributeError:
            return False


class Path(PandasProfilingBaseType):
    @classmethod
    def get_relations(cls):
        relations = [IdentityRelation(cls, Categorical)]
        return relations

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        try:
            return all(os.path.isabs(p) for p in series)
        except TypeError:
            return False


class File(PandasProfilingBaseType):
    @classmethod
    def get_relations(cls):
        relations = [IdentityRelation(cls, Path)]
        return relations

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        return all(os.path.exists(p) for p in series)


class Image(PandasProfilingBaseType):
    @classmethod
    def get_relations(cls):
        relations = [IdentityRelation(cls, File)]
        return relations

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        return all(imghdr.what(p) for p in series)


class Complex(PandasProfilingBaseType):
    @classmethod
    def get_relations(cls):
        return [IdentityRelation(cls, Numeric)]

    @classmethod
    @nullable_series_contains
    def contains_op(cls, series: pd.Series) -> bool:
        return pdt.is_complex_dtype(series)


class ProfilingTypeSet(VisionsTypeset):
    def __init__(self):
        types = {
            Unsupported,
            Boolean,
            Numeric,
            Categorical,
            DateTime,
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
