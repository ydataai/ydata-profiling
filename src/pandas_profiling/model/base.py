"""Common parts to all other modules, mainly utility functions."""
import imghdr
import os
from enum import Enum, unique
from urllib.parse import ParseResult, urlparse

import numpy as np
import pandas as pd

from pandas_profiling.config import config

from visions import (Categorical, Boolean, Float, DateTime, URL, Complex, Path, File, Image, Integer, Generic,
                     Object, String)

from visions.typesets.typeset import VisionsTypeset
from visions.relations import IdentityRelation, InferenceRelation, TypeRelation
import visions as vis



class Numeric(vis.types.VisionsBaseType):
    """**Numeric** implementation of :class:`visions.types.type.VisionsBaseType`.

    Examples:
        >>> x = pd.Series([1, 2, 3])
        >>> x in visions.Integer
        True
    """

    @classmethod
    def get_relations(cls):
        relations = [
            IdentityRelation(cls, Generic),
        ]
        return relations

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        return pd.api.types.is_numeric_dtype(series)


PP_bool_map = [{'yes': True, 'no': False},
                {'y': True, 'n': False},
                {'true': True, 'false': False},
                {'t': True, 'f': False}]
Bool = vis.Boolean.make_string_coercion('PP', PP_bool_map)


class ProfilingTypeSet(VisionsTypeset):
    """Base typeset for pandas-profiling"""
    def __init__(self):
  
        types = {
            Bool,
            Numeric,
            Integer,
            Float,
            DateTime,
            URL,
            Complex,
            Path,
            Object,
            String,
        }

        if config["vars"]["file"]["active"].get(bool):
            types.add(File)
            if config["vars"]["image"]["active"].get(bool):
                types.add(Image)

        super().__init__(types)


@unique
class Variable(Enum):
    """The possible types of variables in the Profiling Report."""

    TYPE_CAT = "CAT"
    """A categorical variable"""

    TYPE_BOOL = Bool
    """A boolean variable"""

    TYPE_NUM = Numeric
    """A numeric variable"""

    TYPE_DATE = DateTime
    """A date variable"""

    TYPE_URL = URL
    """A URL variable"""

    TYPE_COMPLEX = Complex
    """A Complex variable"""

    TYPE_PATH = Path
    """Absolute path"""

    TYPE_FILE = File
    """File (i.e. existing path)"""

    TYPE_IMAGE = Image
    """Images"""

    S_TYPE_UNSUPPORTED = Generic
    """An unsupported variable"""

    #TYPE_REAL = TYPE_NUM

    #TYPE_COUNT = TYPE_NUM

    #TYPE_ABSOLUTEPATH = TYPE_PATH

    #TYPE_FILEPATH = TYPE_FILE

    #TYPE_IMAGEPATH = TYPE_IMAGE

    #TYPE_GENERIC = S_TYPE_UNSUPPORTED

    @classmethod
    def get_by_value(cls, value):
        for val in cls:
            if val.value == value:
                return val
        
        raise ValueError(f"No value {value}")


def get_counts(series: pd.Series) -> dict:
    """Counts the values in a series (with and without NaN, distinct).

    Args:
        series: Series for which we want to calculate the values.

    Returns:
        A dictionary with the count values (with and without NaN, distinct).
    """
    value_counts_with_nan = series.value_counts(dropna=False)
    value_counts_without_nan = (
        value_counts_with_nan.reset_index().dropna().set_index("index").iloc[:, 0]
    )

    distinct_count_with_nan = value_counts_with_nan.count()
    distinct_count_without_nan = value_counts_without_nan.count()

    def infinity_test():
        try:
            return any(x in value_counts_with_nan for x in [np.inf, -np.inf])
        except:
            return False
    
    return {
        "value_counts": value_counts_without_nan,  # Alias
        "value_counts_with_nan": value_counts_with_nan,
        "value_counts_without_nan": value_counts_without_nan,
        "distinct_count_with_nan": distinct_count_with_nan,
        "distinct_count_without_nan": distinct_count_without_nan,
        "has_inf": infinity_test(),
    }


def is_boolean(series: pd.Series, series_description: dict) -> bool:
    """Is the series boolean type?

    Args:
        series: Series
        series_description: Series description

    Returns:
        True is the series is boolean type in the broad sense (e.g. including yes/no, NaNs allowed).
    """
    keys = series_description["value_counts_without_nan"].keys()
    if pd.api.types.is_bool_dtype(keys):
        return True
    elif (
        1 <= series_description["distinct_count_without_nan"] <= 2
        and pd.api.types.is_numeric_dtype(series)
        and series[~series.isnull()].between(0, 1).all()
    ):
        return True
    elif 1 <= series_description["distinct_count_without_nan"] <= 4:
        unique_values = set([str(value).lower() for value in keys.values])
        accepted_combinations = [
            ["y", "n"],
            ["yes", "no"],
            ["true", "false"],
            ["t", "f"],
        ]

        if len(unique_values) == 2 and any(
            [unique_values == set(bools) for bools in accepted_combinations]
        ):
            return True

    return False


def is_numeric(series: pd.Series, series_description: dict) -> bool:
    """Is the series numeric type?

    Args:
        series: Series
        series_description: Series description

    Returns:
        True is the series is numeric type (NaNs allowed).
    """
    return pd.api.types.is_numeric_dtype(series) and (
        series_description["distinct_count_without_nan"]
        >= config["vars"]["num"]["low_categorical_threshold"].get(int)
        or any(np.inf == s or -np.inf == s for s in series)
    )


def is_url(series: pd.Series, series_description: dict) -> bool:
    """Is the series url type?

    Args:
        series: Series
        series_description: Series description

    Returns:
        True is the series is url type (NaNs allowed).
    """

    def is_url_item(x):
        return isinstance(x, ParseResult) and all((x.netloc, x.scheme, x.path))

    if series_description["distinct_count_without_nan"] > 0:
        try:
            result = series[~series.isnull()].astype(str)
            return all(is_url_item(urlparse(x)) for x in result)
        except ValueError:
            return False
    else:
        return False


def is_path(series, series_description) -> bool:
    """Is the series of the path type (i.e. absolute path)?

    Args:
        series: Series
        series_description: Series description

    Returns:
        True is the series is path type (NaNs allowed).
    """
    if series_description["distinct_count_without_nan"] == 0:
        return False

    try:
        result = series[~series.isnull()].astype(str)
        return all(os.path.isabs(p) for p in result)
    except (ValueError, TypeError):
        return False


def is_file(series, series_description) -> bool:
    """Is the series of the type "file" (i.e. existing paths)?

    Args:
        series: Series
        series_description: Series description

    Returns:
        True is the series is of the file type (NaNs allowed).
    """
    if series_description["distinct_count_without_nan"] == 0:
        return False

    try:
        result = series[~series.isnull()].astype(str)
        return all(os.path.exists(p) for p in result)
    except (ValueError, TypeError):
        return False


def is_image(series, series_description) -> bool:
    """Is the series of the image type (i.e. "file" with image extensions)?

    Args:
        series: Series
        series_description: Series description

    Returns:
        True is the series is of the image type (NaNs allowed).
    """
    if series_description["distinct_count_without_nan"] > 0:
        try:
            result = series[~series.isnull()].astype(str)
            return all(imghdr.what(p) for p in result)
        except (TypeError, ValueError):
            return False
    else:
        return False


def is_date(series) -> bool:
    """Is the variable of type datetime? Throws a warning if the series looks like a datetime, but is not typed as
    datetime64.

    Args:
        series: Series

    Returns:
        True if the variable is of type datetime.
    """
    is_date_value = pd.api.types.is_datetime64_dtype(series)

    return is_date_value


def get_var_type(series: pd.Series) -> dict:
    """Get the variable type of a series.

    Args:
        series: Series for which we want to infer the variable type.

    Returns:
        The series updated with the variable type included.
    """

    series_description = {}
    typeset = ProfilingTypeSet()
    # TODO: Remove this big try block
    try:
        series_description = get_counts(series)
    except TypeError:
        var_type = Variable.S_TYPE_UNSUPPORTED
        series_description.update({"type": var_type})
        return series_description
    
    # When the inferred type of the index is just "mixed" probably the types within the series are tuple, dict,
    # list and so on...
    if series_description["value_counts_without_nan"].index.inferred_type.startswith("mixed"):
        raise TypeError("Not supported mixed type")
    
    if series_description["distinct_count_without_nan"] == 0:
        var_type = Variable.S_TYPE_UNSUPPORTED
    else:
        var_type = typeset.infer_series_type(series)
        if var_type is Integer or var_type is Float:
            var_type = Numeric

        if var_type not in [x.value for x in Variable]:
            var_type = Variable.TYPE_CAT
        else:
            var_type = Variable.get_by_value(var_type)

    if var_type is Variable.TYPE_NUM:
        categorical_threshold = config["vars"]["num"]["low_categorical_threshold"].get(int)
        disctinct_count = series_description["distinct_count_without_nan"]
        
        if (disctinct_count < categorical_threshold) and not series_description["has_inf"]:
            var_type = Variable.TYPE_CAT

    series_description.update({"type": var_type})
    return series_description
