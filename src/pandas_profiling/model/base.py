"""Common parts to all other modules, mainly utility functions."""
import imghdr
import os
from enum import Enum, unique
from urllib.parse import ParseResult, urlparse

import numpy as np
import pandas as pd

from pandas_profiling.config import config
from pandas_profiling.model.typeset import ProfilingTypeSet, Object


typeset = ProfilingTypeSet()


def get_counts(series: pd.Series) -> dict:
    """Counts the values in a series (with and without NaN, distinct).

    Args:
        series: Series for which we want to calculate the values.

    Returns:
        A dictionary with the count values (with and without NaN, distinct).
    """
    series_summary = {'hashable': True}
    series_summary['value_counts_with_nan'] = series.value_counts(dropna=False)
                                                            
    series_summary['value_counts_without_nan'] = (
        series_summary['value_counts_with_nan'].reset_index().dropna().set_index("index").iloc[:, 0]
    )

    series_summary['distinct_count_with_nan'] = series_summary['value_counts_with_nan'].count()
    series_summary['distinct_count_without_nan'] = series_summary['value_counts_without_nan'].count()
    
    # TODO: No need for duplication here, refactor
    series_summary['value_counts'] = series_summary['value_counts_without_nan']
    try:
        set(series_summary['value_counts_with_nan'].index)
    except:
        series_summary['hashable'] = False

    return series_summary


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

    series_description = get_counts(series)
    series_description['type'] = typeset.detect_series_type(series)
    return series_description
