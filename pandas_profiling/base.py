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

def get_vartype(data):
    """Infer the type of a variable (technically a Series).

    The types supported are split in standard types and special types.

    Standard types:
        * Categorical (`TYPE_CAT`): the default type if no other one can be determined
        * Numerical (`TYPE_NUM`): if it contains numbers
        * Boolean (`TYPE_BOOL`): at this time only detected if it contains boolean values, see todo
        * Date (`TYPE_DATE`): if it contains datetime

    Special types:
        * Constant (`S_TYPE_CONST`): if all values in the variable are equal
        * Unique (`S_TYPE_UNIQUE`): if all values in the variable are different

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
        * distinct_count shall not be computed several times since it can be time consuming
        * Boolean type could be infered also for other pairs of binaries values (1/0, Y/N, etc.)
        * #72: Numeric with low Distinct count should be treated as "Categorical"
    """
    distinct_count = data.nunique(dropna=False)
    leng = len(data)
    if distinct_count <= 1:
        return S_TYPE_CONST
    elif pd.api.types.is_bool_dtype(data):
        return TYPE_BOOL
    elif pd.api.types.is_numeric_dtype(data):
        return TYPE_NUM
    elif pd.api.types.is_datetime64_dtype(data):
        return TYPE_DATE
    elif distinct_count == leng:
        return S_TYPE_UNIQUE
    else:
        return TYPE_CAT
