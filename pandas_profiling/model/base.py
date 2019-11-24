"""Common parts to all other modules, mainly utility functions."""
import sys

import pandas as pd
from enum import Enum, unique
from urllib.parse import urlparse


from pandas_profiling.config import config
from pandas_profiling.utils.data_types import str_is_path


@unique
class Variable(Enum):
    """The possible types of variables in the Profiling Report."""

    TYPE_CAT = "CAT"
    """A categorical variable"""

    TYPE_BOOL = "BOOL"
    """A boolean variable"""

    TYPE_NUM = "NUM"
    """A numeric variable"""

    TYPE_DATE = "DATE"
    """A date variable"""

    TYPE_URL = "URL"
    """A URL variable"""

    TYPE_PATH = "PATH"
    """Absolute files"""

    S_TYPE_CONST = "CONST"
    """A constant variable"""

    S_TYPE_UNIQUE = "UNIQUE"
    """An unique variable"""

    S_TYPE_UNSUPPORTED = "UNSUPPORTED"
    """An unsupported variable"""

    S_TYPE_CORR = "CORR"
    """A highly correlated variable"""

    S_TYPE_RECODED = "RECODED"
    """A recorded variable"""

    S_TYPE_REJECTED = "REJECTED"
    """A rejected variable"""


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

    # When the inferred type of the index is just "mixed" probably the types within the series are tuple, dict,
    # list and so on...
    if value_counts_without_nan.index.inferred_type == "mixed":
        raise TypeError("Not supported mixed type")

    return {
        "value_counts_with_nan": value_counts_with_nan,
        "value_counts_without_nan": value_counts_without_nan,
        "distinct_count_with_nan": distinct_count_with_nan,
        "distinct_count_without_nan": distinct_count_without_nan,
    }


def is_boolean(series: pd.Series, series_description: dict) -> bool:
    """Is the series boolean type?

    Args:
        series: Series
        series_description: Series description

    Returns:
        True if the series is boolean type in the broad sense (e.g. including yes/no, NaNs allowed).
    """
    keys = series_description["value_counts_without_nan"].keys()
    if pd.api.types.is_bool_dtype(keys):
        return True
    elif (
        series_description["distinct_count_without_nan"] <= 2
        and pd.api.types.is_numeric_dtype(series)
        and series[~series.isnull()].between(0, 1).all()
    ):
        return True
    elif series_description["distinct_count_without_nan"] <= 4:
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
        True if the series is numeric type (NaNs allowed).
    """
    return pd.api.types.is_numeric_dtype(series) and series_description[
        "distinct_count_without_nan"
    ] >= config["low_categorical_threshold"].get(int)


def is_url(series: pd.Series, series_description: dict) -> bool:
    """Is the series url type?

    Args:
        series: Series
        series_description: Series description

    Returns:
        True if the series is url type (NaNs allowed).
    """
    if series_description["distinct_count_without_nan"] > 0:
        try:
            result = series[~series.isnull()].astype(str).apply(urlparse)
            return result.apply(lambda x: all([x.scheme, x.netloc, x.path])).all()
        except ValueError:
            return False
    else:
        return False


def is_path(series, series_description) -> bool:
    if series_description["distinct_count_without_nan"] > 0:
        try:
            result = series[~series.isnull()].astype(str).apply(str_is_path)
            return result.all()
        except ValueError:
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

    try:
        series_description = get_counts(series)

        distinct_count_with_nan = series_description["distinct_count_with_nan"]
        distinct_count_without_nan = series_description["distinct_count_without_nan"]

        if distinct_count_with_nan <= 1:
            var_type = Variable.S_TYPE_CONST
        elif is_boolean(series, series_description):
            var_type = Variable.TYPE_BOOL
        elif is_numeric(series, series_description):
            var_type = Variable.TYPE_NUM
        elif is_date(series):
            var_type = Variable.TYPE_DATE
        elif is_url(series, series_description):
            var_type = Variable.TYPE_URL
        elif is_path(series, series_description) and sys.version_info[1] > 5:
            var_type = Variable.TYPE_PATH
        elif distinct_count_without_nan == len(series):
            var_type = Variable.S_TYPE_UNIQUE
        else:
            var_type = Variable.TYPE_CAT
    except TypeError:
        series_description = {}
        var_type = Variable.S_TYPE_UNSUPPORTED

    series_description.update({"type": var_type})

    return series_description
