# -*- coding: utf-8 -*-
"""Common parts to all other modules, mainly utility functions.
"""
import pandas as pd

TYPE_CAT = 'CAT'
"""String: A categorical variable"""

TYPE_BOOL = 'BOOL'
"""String: A boolean variable"""

TYPE_NUM = 'NUM'
"""String: A numerical variable"""

TYPE_DATE = 'DATE'
"""String: A numeric variable"""

S_TYPE_CONST = 'CONST'
"""String: A constant variable"""

S_TYPE_UNIQUE = 'UNIQUE'
"""String: A unique variable"""

S_TYPE_UNSUPPORTED = 'UNSUPPORTED'
"""String: An unsupported variable"""

value_counts_memo = {}
def get_groupby_statistic(data):
    """Calculate value counts and distinct count of a variable (technically a Series) caching the results by column name.
    Parameters
    ----------
    data : Series
        The data type of the Series.

    Returns
    -------
    str
        The data type of the Series.
    """
    if data.name is not None and data.name in value_counts_memo:
        return value_counts_memo[data.name]

    value_counts_with_nan = data.value_counts(dropna=False)
    value_counts_without_nan = value_counts_with_nan.loc[value_counts_with_nan.index.dropna()]
    distinct_count_with_nan = value_counts_with_nan.count()

    # When the inferred type of the index is just "mixed" probably the types within the series are tuple, dict, list and so on...
    if value_counts_without_nan.index.inferred_type == "mixed":
        raise TypeError('Not supported mixed type')

    result = [value_counts_without_nan, distinct_count_with_nan]

    if data.name is not None:
        value_counts_memo[data.name] = result

    return result

memo = {}
def get_vartype(data):
    """Infer the type of a variable (technically a Series) caching the results by column name.

    The types supported are split in standard types and special types.

    Standard types:
        * Categorical (`TYPE_CAT`): the default type if no other one can be determined
        * Numerical (`TYPE_NUM`): if it contains numbers
        * Boolean (`TYPE_BOOL`): at this time only detected if it contains boolean values, see todo
        * Date (`TYPE_DATE`): if it contains datetime

    Special types:
        * Constant (`S_TYPE_CONST`): if all values in the variable are equal
        * Unique (`S_TYPE_UNIQUE`): if all values in the variable are different
        * Unsupported (`S_TYPE_UNSUPPORTED`): if the variable is unsupported

    Parameters
    ----------
    data : Series
        The data type of the Series.

    Returns
    -------
    str
        The data type of the Series.

    Notes
    ----
        * Should improve verification when a categorical or numeric field has 3 values, it could be a categorical field
        or just a boolean with NaN values
        * #72: Numeric with low Distinct count should be treated as "Categorical"
    """
    if data.name is not None and data.name in memo:
        return memo[data.name]

    type = None
    try:
        value_counts, distinct_count = get_groupby_statistic(data)
        leng = len(data)

        if distinct_count <= 1:
            type = S_TYPE_CONST
        elif pd.api.types.is_bool_dtype(data) or (distinct_count == 2 and pd.api.types.is_numeric_dtype(data)):
            type = TYPE_BOOL
        elif pd.api.types.is_numeric_dtype(data):
            type = TYPE_NUM
        elif pd.api.types.is_datetime64_dtype(data):
            type = TYPE_DATE
        elif distinct_count == leng:
            type = S_TYPE_UNIQUE
        else:
            type = TYPE_CAT
    except:
        type = S_TYPE_UNSUPPORTED

    if data.name is not None:
        memo[data.name] = type

    return type

def clear_cache():
    global memo, value_counts_memo
    memo = {}
    value_counts_memo = {}
