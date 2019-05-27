"""Common parts to all other modules, mainly utility functions."""
import pandas as pd
from enum import Enum, unique


@unique
class Variable(Enum):
    """The possible types of variables in the Profiling Report."""

    TYPE_CAT: str = "CAT"
    """A categorical variable"""

    TYPE_BOOL: str = "BOOL"
    """A boolean variable"""

    TYPE_NUM: str = "NUM"
    """A numeric variable"""

    TYPE_DATE: str = "DATE"
    """A date variable"""

    S_TYPE_CONST: str = "CONST"
    """A constant variable"""

    S_TYPE_UNIQUE: str = "UNIQUE"
    """An unique variable"""

    S_TYPE_UNSUPPORTED: str = "UNSUPPORTED"
    """An unsupported variable"""

    S_TYPE_CORR: str = "CORR"
    """A highly correlated variable"""

    S_TYPE_RECODED: str = "RECODED"
    """A recorded variable"""

    S_TYPE_REJECTED: str = "REJECTED"
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

    # When the inferred type of the index is just "mixed" probably the types within the series are tuple, dict,
    # list and so on...
    if value_counts_without_nan.index.inferred_type == "mixed":
        raise TypeError("Not supported mixed type")

    return {
        "value_counts_with_nan": value_counts_with_nan,
        "value_counts_without_nan": value_counts_without_nan,
        "distinct_count_with_nan": distinct_count_with_nan,
    }


def get_var_type(series: pd.Series) -> dict:
    """Get the variable type of a series.

    Args:
        series: Series for which we want to infer the variable type.

    Returns:
        The series updated with the variable type included.
    """
    # TODO: Should improve verification when a categorical or numeric field has 3 values, it could be a categorical
    #  field or just a boolean with NaN values
    # TODO: Numeric with low Distinct count should be treated as "Categorical"
    # TODO: distinct count without NaN

    try:
        series_description = get_counts(series)
        # TODO: check if we prefer with or without nan
        distinct_count_without_nan = series_description["distinct_count_with_nan"]

        if distinct_count_without_nan <= 1:
            var_type = Variable.S_TYPE_CONST
        elif pd.api.types.is_bool_dtype(series) or (
            distinct_count_without_nan == 2 and pd.api.types.is_numeric_dtype(series)
        ):
            var_type = Variable.TYPE_BOOL
        elif pd.api.types.is_numeric_dtype(series):
            var_type = Variable.TYPE_NUM
        elif pd.api.types.is_datetime64_dtype(series):
            var_type = Variable.TYPE_DATE
        elif distinct_count_without_nan == len(series):
            var_type = Variable.S_TYPE_UNIQUE
        else:
            var_type = Variable.TYPE_CAT
    except TypeError:
        series_description = {}
        var_type = Variable.S_TYPE_UNSUPPORTED

    series_description.update({"type": var_type})

    return series_description
