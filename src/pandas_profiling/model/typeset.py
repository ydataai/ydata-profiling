import imghdr
import os
import warnings
from urllib.parse import urlparse

import pandas as pd
import visions
from pandas.api import types as pdt
from visions import VisionsBaseType, VisionsTypeset
from visions.relations import IdentityRelation, InferenceRelation
from visions.utils import nullable_series_contains

from pandas_profiling.config import config
from pandas_profiling.model.typeset_relations import (
    category_is_numeric,
    category_to_numeric,
    numeric_is_category,
    series_is_string,
    string_is_bool,
    string_to_bool,
    to_bool,
    to_category,
)


class PandasProfilingBaseType(VisionsBaseType):
    pass


class Unsupported(PandasProfilingBaseType, visions.Generic):
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
    @nullable_series_contains
    def contains_op(cls, series: pd.Series) -> bool:
        return pdt.is_numeric_dtype(series) and not pdt.is_bool_dtype(series)


def is_date(series):
    try:
        _ = pd.to_datetime(series)
        return True
    except:
        return False


def to_date(series):
    return pd.to_datetime(series)


class DateTime(PandasProfilingBaseType):
    @classmethod
    def get_relations(cls):
        return [
            IdentityRelation(cls, Unsupported),
            # TODO: optional
            # TODO: coerce
            # InferenceRelation(cls, Categorical, relationship=is_date, transformer=to_date),
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
                transformer=to_category,
            ),
        ]

    @classmethod
    @nullable_series_contains
    def contains_op(cls, series: pd.Series) -> bool:
        is_valid_dtype = pdt.is_categorical_dtype(series) and not pdt.is_bool_dtype(
            series
        )
        if is_valid_dtype:
            return True

        return series_is_string(series)


class Boolean(PandasProfilingBaseType):
    @classmethod
    def get_relations(cls):
        return [
            IdentityRelation(cls, Unsupported),
            # TODO: optional + values
            InferenceRelation(
                cls,
                Categorical,
                relationship=string_is_bool,
                transformer=lambda s: to_bool(string_to_bool(s)),
            ),
            # TODO: optional numeric
        ]

    @classmethod
    @nullable_series_contains
    def contains_op(cls, series: pd.Series) -> bool:
        if pdt.is_object_dtype(series):
            try:
                return series.isin({True, False}).all()
            except:
                return False

        return pdt.is_bool_dtype(series)


class URL(PandasProfilingBaseType):
    @classmethod
    def get_relations(cls):
        relations = [IdentityRelation(cls, Categorical)]
        return relations

    @classmethod
    @nullable_series_contains
    def contains_op(cls, series: pd.Series) -> bool:
        # TODO: use coercion utils
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
    @nullable_series_contains
    def contains_op(cls, series: pd.Series) -> bool:
        # TODO: use coercion utils
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
    @nullable_series_contains
    def contains_op(cls, series: pd.Series) -> bool:
        return all(os.path.exists(p) for p in series)


class Image(PandasProfilingBaseType):
    @classmethod
    def get_relations(cls):
        relations = [IdentityRelation(cls, File)]
        return relations

    @classmethod
    @nullable_series_contains
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

        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=UserWarning)
            super().__init__(types)


if __name__ == "__main__":
    from matplotlib import pyplot as plt

    config.set_arg_group("explorative")
    ts = ProfilingTypeSet()
    ts.plot_graph()
    plt.show()
