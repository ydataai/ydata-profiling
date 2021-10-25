import warnings

import numpy as np
import pandas as pd

from pandas_profiling.config import Settings
from pandas_profiling.model.dataframe import check_dataframe, preprocess
from pandas_profiling.utils.dataframe import rename_index


@check_dataframe.register
def pandas_check_dataframe(df: pd.DataFrame) -> None:
    if not isinstance(df, pd.DataFrame):
        warnings.warn("df is not of type pandas.DataFrame")


@preprocess.register
def pandas_preprocess(config: Settings, df: pd.DataFrame) -> pd.DataFrame:
    """Preprocess the dataframe

    - Drops the index if `include_index` is False
    - Otherwise, appends the index to the dataframe when it contains information
    - Rename the "index" column to "df_index", if exists
    - Convert the DataFrame's columns to str

    Args:
        config: report Settings object
        df: the pandas DataFrame

    Returns:
        The preprocessed DataFrame
    """
    # Drop index if config specifies
    if not config.include_index:
        df = df.reset_index(drop=True)

    # Treat index as any other column
    elif (
        not pd.Index(np.arange(0, len(df))).equals(df.index)
        or df.index.dtype != np.int64
    ):
        df = df.reset_index()

    # Rename reserved column names
    df = rename_index(df)

    # Ensure that columns are strings
    df.columns = df.columns.astype("str")
    return df
