from functools import singledispatch
from typing import Optional

import pandas as pd

from pandas_profiling.config import config
from pandas_profiling.model.dataframe_wrappers import (
    GenericDataFrame,
    PandasDataFrame,
    SparkDataFrame,
)


@singledispatch
def get_duplicates(df: GenericDataFrame, supported_columns) -> Optional[pd.DataFrame]:
    raise NotImplementedError("This method is not implemented ")


@get_duplicates.register(PandasDataFrame)
def _get_duplicates_pandas(
    df: PandasDataFrame, supported_columns
) -> Optional[pd.DataFrame]:
    """Obtain the most occurring duplicate rows in the DataFrame.

    Args:
        df: the Pandas DataFrame.
        supported_columns: the columns to consider

    Returns:
        A subset of the DataFrame, ordered by occurrence.
    """
    n_head = config["duplicates"]["head"].get(int)

    if n_head > 0 and supported_columns:
        return df.groupby_get_n_largest_dups(supported_columns, n_head)

    return None


@get_duplicates.register(SparkDataFrame)
def _get_duplicates_spark(
    df: SparkDataFrame, supported_columns
) -> Optional[pd.DataFrame]:
    """Obtain the most occurring duplicate rows in the DataFrame.

    Args:
        df: the Pandas DataFrame.
        supported_columns: the columns to consider

    Returns:
        A subset of the DataFrame, ordered by occurrence.
    """
    n_head = config["duplicates"]["head"].get(int)

    if n_head > 0 and supported_columns:
        return df.groupby_get_n_largest_dups(supported_columns, n_head)

    return None
