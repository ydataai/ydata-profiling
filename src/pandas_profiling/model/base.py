"""Common parts to all other modules, mainly utility functions."""
import sys
from enum import Enum, unique
from urllib.parse import ParseResult, urlparse

import numpy as np
import pandas as pd

from pandas_profiling.config import config


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

    TYPE_COMPLEX = "COMPLEX"

    S_TYPE_UNSUPPORTED = "UNSUPPORTED"
    """An unsupported variable"""


# Temporary mapping
Boolean = Variable.TYPE_BOOL
Real = Variable.TYPE_NUM
Count = Variable.TYPE_NUM
Complex = Variable.TYPE_COMPLEX
Date = Variable.TYPE_DATE
Categorical = Variable.TYPE_CAT
Url = Variable.TYPE_URL
AbsolutePath = Variable.TYPE_PATH
ExistingPath = Variable.TYPE_PATH
ImagePath = Variable.TYPE_PATH
Generic = Variable.S_TYPE_UNSUPPORTED


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

    return {
        "value_counts": value_counts_without_nan,  # Alias
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
    from pathlib import Path

    def is_path_item(p: str):
        """Detects if the variable contains absolute paths. If so, we distinguish paths that exist and paths that are images.

        Args:
            p: the Path

        Returns:
            True is is an absolute path
        """
        try:
            path = Path(p)
            if path.is_absolute():
                return True
            else:
                return False
        except TypeError:
            return False

    if series_description["distinct_count_without_nan"] > 0:
        try:
            result = series[~series.isnull()].astype(str)
            return all(is_path_item(x) for x in result)
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

    series_description = {}

    try:
        series_description = get_counts(series)

        # When the inferred type of the index is just "mixed" probably the types within the series are tuple, dict,
        # list and so on...
        if series_description[
            "value_counts_without_nan"
        ].index.inferred_type.startswith("mixed"):
            raise TypeError("Not supported mixed type")

        if series_description["distinct_count_without_nan"] == 0:
            # Empty
            var_type = Variable.S_TYPE_UNSUPPORTED
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
        else:
            var_type = Variable.TYPE_CAT
    except TypeError:
        var_type = Variable.S_TYPE_UNSUPPORTED

    series_description.update({"type": var_type})

    return series_description
