from functools import singledispatch
from typing import List, Optional

import pandas as pd

from pandas_profiling.model.dataframe_wrappers import (
    GenericDataFrame,
    PandasDataFrame,
    SparkDataFrame,
)


@singledispatch
def get_duplicates(
    df: GenericDataFrame, supported_columns, n_head
) -> Optional[pd.DataFrame]:
    raise NotImplementedError("This method is not implemented.")


@get_duplicates.register(PandasDataFrame)
def _get_duplicates_pandas(
    df: PandasDataFrame, supported_columns: List[str], n_head: int
) -> Optional[pd.DataFrame]:
    """Obtain the most occurring duplicate rows in the DataFrame.

    Args:
        df: the Pandas DataFrame.
        supported_columns: the columns to consider
        n_head: top n duplicate values to return

    Returns:
        A subset of the DataFrame, ordered by occurrence.
    """
    return df.groupby_get_n_largest_dups(supported_columns, n_head)


@get_duplicates.register(SparkDataFrame)
def _get_duplicates_spark(
    df: SparkDataFrame, supported_columns: List[str], n_head: int
) -> Optional[pd.DataFrame]:
    """Obtain the most occurring duplicate rows in the DataFrame.

    Args:
        df: the Pandas DataFrame.
        supported_columns: the columns to consider
        n_head: top n duplicate values to return

    Returns:
        A subset of the DataFrame, ordered by occurrence.
    """
    return df.groupby_get_n_largest_dups(supported_columns, n_head)
