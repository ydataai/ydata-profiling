import imghdr
import os
import warnings
from urllib.parse import urlparse

import pandas as pd
import visions
from multimethod import multimethod
from pandas.api import types as pdt
from visions.backends.pandas.series_utils import series_handle_nulls, series_not_empty
from visions.relations import IdentityRelation, InferenceRelation

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

pandas_has_string_dtype_flag = hasattr(pdt, "is_string_dtype")


class Unsupported(visions.Generic):
    pass


class Numeric(visions.VisionsBaseType):
    @staticmethod
    def get_relations():
        return [
            IdentityRelation(Unsupported),
            InferenceRelation(
                Categorical,
                relationship=category_is_numeric,
                transformer=category_to_numeric,
            ),
        ]

    @staticmethod
    @multimethod
    @series_not_empty
    @series_handle_nulls
    def contains_op(series: pd.Series, state: dict) -> bool:
        return pdt.is_numeric_dtype(series) and not pdt.is_bool_dtype(series)


def is_date(series, state):
    try:
        _ = pd.to_datetime(series)
        return True
    except:  # noqa: E722
        return False


def to_date(series):
    return pd.to_datetime(series)


class DateTime(visions.VisionsBaseType):
    @staticmethod
    def get_relations():
        return [
            IdentityRelation(Unsupported),
        ]

    @staticmethod
    @multimethod
    @series_not_empty
    @series_handle_nulls
    def contains_op(series: pd.Series, state: dict) -> bool:
        return pdt.is_datetime64_any_dtype(series)


class Categorical(visions.VisionsBaseType):
    @staticmethod
    def get_relations():
        return [
            IdentityRelation(Unsupported),
            InferenceRelation(
                Numeric,
                relationship=numeric_is_category,
                transformer=to_category,
            ),
        ]

    @staticmethod
    @multimethod
    @series_not_empty
    @series_handle_nulls
    def contains_op(series: pd.Series, state: dict) -> bool:
        is_valid_dtype = pdt.is_categorical_dtype(series) and not pdt.is_bool_dtype(
            series
        )
        if is_valid_dtype:
            return True
        elif not pdt.is_object_dtype(series):
            return pandas_has_string_dtype_flag and pdt.is_string_dtype(series)

        return series_is_string(series, state)


class Boolean(visions.VisionsBaseType):
    @staticmethod
    def get_relations():
        # Numeric [0, 1] goes via Categorical with distinct_count_without_nan <= 2
        return [
            IdentityRelation(Unsupported),
            InferenceRelation(
                Categorical,
                relationship=string_is_bool,
                transformer=lambda s, st: to_bool(string_to_bool(s, st)),
            ),
        ]

    @staticmethod
    @multimethod
    @series_not_empty
    @series_handle_nulls
    def contains_op(series: pd.Series, state: dict) -> bool:
        if pdt.is_object_dtype(series):
            try:
                return series.isin({True, False}).all()
            except:  # noqa: E722
                return False

        return pdt.is_bool_dtype(series)


class URL(visions.VisionsBaseType):
    @staticmethod
    def get_relations():
        return [IdentityRelation(Categorical)]

    @staticmethod
    @multimethod
    @series_handle_nulls
    def contains_op(series: pd.Series, state: dict) -> bool:
        # TODO: use coercion utils
        try:
            url_gen = (urlparse(x) for x in series)
            return all(x.netloc and x.scheme for x in url_gen)
        except AttributeError:
            return False


class Path(visions.VisionsBaseType):
    @staticmethod
    def get_relations():
        return [IdentityRelation(Categorical)]

    @staticmethod
    @multimethod
    @series_handle_nulls
    def contains_op(series: pd.Series, state: dict) -> bool:
        # TODO: use coercion utils
        try:
            return all(os.path.isabs(p) for p in series)
        except TypeError:
            return False


class File(visions.VisionsBaseType):
    @staticmethod
    def get_relations():
        return [IdentityRelation(Path)]

    @staticmethod
    @multimethod
    @series_handle_nulls
    def contains_op(series: pd.Series, state: dict) -> bool:
        return all(os.path.exists(p) for p in series)


class Image(visions.VisionsBaseType):
    @staticmethod
    def get_relations():
        return [IdentityRelation(File)]

    @staticmethod
    @multimethod
    @series_handle_nulls
    def contains_op(series: pd.Series, state: dict) -> bool:
        return all(imghdr.what(p) for p in series)


class Complex(visions.VisionsBaseType):
    @staticmethod
    def get_relations():
        return [IdentityRelation(Numeric)]

    @staticmethod
    @multimethod
    @series_handle_nulls
    def contains_op(series: pd.Series, state: dict) -> bool:
        return pdt.is_complex_dtype(series)


class ProfilingTypeSet(visions.VisionsTypeset):
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
