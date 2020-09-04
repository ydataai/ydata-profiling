import imghdr
import os

import pandas as pd
import visions
from pandas.api import types as pdt
from visions import VisionsBaseType, VisionsTypeset
from visions.relations import IdentityRelation, InferenceRelation
from visions.types.url import test_url, to_url
from visions.utils import nullable_series_contains

from pandas_profiling.config import config

# class ProfilingTypeCategories:
#     continuous = False
#     categorical = False


class PandasProfilingBaseType(VisionsBaseType):
    pass


class Unsupported(visions.Generic):
    pass


class Numeric(PandasProfilingBaseType):
    @classmethod
    def get_relations(cls):
        return [
            IdentityRelation(cls, Unsupported),
        ]

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        return not pdt.is_bool_dtype(series) and pdt.is_numeric_dtype(series)


class DateTime(PandasProfilingBaseType):
    @classmethod
    def get_relations(cls):
        return [
            IdentityRelation(cls, Unsupported),
        ]

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        return pdt.is_datetime64_dtype(series)


class Categorical(PandasProfilingBaseType):
    @classmethod
    def get_relations(cls):
        return [
            IdentityRelation(cls, Unsupported),
            # InferenceRelation(
            #     cls,
            #     Numeric,
            #     relationship=lambda s: s.nunique()
            #     < config["vars"]["num"]["low_categorical_threshold"].get(int),
            #     transformer=applied_to_nonnull(lambda s: s.astype(str)),
            # ),
        ]

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        is_valid_dtype = pdt.is_categorical_dtype(series)
        if is_valid_dtype:
            return True

        if series.hasnans:
            series = series.dropna()
            if series.empty:
                return False
        return all(isinstance(v, str) for v in series)


class Boolean(PandasProfilingBaseType):
    @classmethod
    def get_relations(cls):
        return [
            IdentityRelation(cls, Categorical),
            # InferenceRelation(
            #     cls,
            #     Numeric,
            #     relationship=lambda s: s.nunique()
            #     < config["vars"]["num"]["low_categorical_threshold"].get(int),
            #     transformer=applied_to_nonnull(lambda s: s.astype(str)),
            # ),
        ]

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        return pdt.is_bool_dtype(series)


class URL(PandasProfilingBaseType):
    @classmethod
    def get_relations(cls):
        relations = [
            IdentityRelation(cls, Categorical),
            InferenceRelation(
                cls, Categorical, relationship=test_url, transformer=to_url
            ),
        ]
        return relations

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        return True


class Path(PandasProfilingBaseType):
    @classmethod
    def get_relations(cls):
        relations = [
            IdentityRelation(cls, Categorical),
            InferenceRelation(
                cls, Categorical, relationship=test_url, transformer=to_url
            ),
        ]
        return relations

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        return all(os.path.isabs(p) for p in series)


class File(PandasProfilingBaseType):
    @classmethod
    def get_relations(cls):
        relations = [
            IdentityRelation(cls, Path),
            InferenceRelation(
                cls, Categorical, relationship=test_url, transformer=to_url
            ),
        ]
        return relations

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        return all(os.path.exists(p) for p in series)


class Image(PandasProfilingBaseType):
    @classmethod
    def get_relations(cls):
        relations = [
            IdentityRelation(cls, File),
            InferenceRelation(
                cls, Categorical, relationship=test_url, transformer=to_url
            ),
        ]
        return relations

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        return all(imghdr.what(p) for p in series)


class Complex(PandasProfilingBaseType):
    @classmethod
    def get_relations(cls):
        return [
            IdentityRelation(cls, Numeric),
        ]

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
