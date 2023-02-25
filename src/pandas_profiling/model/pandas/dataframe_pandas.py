import warnings

import pandas as pd
from pandas_profiling.config import Settings
from pandas_profiling.model.dataframe import check_dataframe, preprocess
from pandas_profiling.utils.dataframe import rename_index


@check_dataframe.register
def pandas_check_dataframe(config: Settings, df: pd.DataFrame) -> None:
    if not isinstance(df, pd.DataFrame):
        warnings.warn("df is not of type pandas.DataFrame")

    # check, if target column is in dataframe
    if config.target.col_name is not None:
        if config.target.col_name not in df:
            raise KeyError(
                f"target column '{config.target.col_name}' is not in dataframe."
            )


@preprocess.register
def pandas_preprocess(df: pd.DataFrame) -> pd.DataFrame:
    """Preprocess the dataframe

    - Appends the index to the dataframe when it contains information
    - Rename the "index" column to "df_index", if exists
    - Convert the DataFrame's columns to str

    Args:
        config: report Settings object
        df: the pandas DataFrame

    Returns:
        The preprocessed DataFrame
    """

    # Rename reserved column names
    df = rename_index(df)

    # Ensure that columns are strings
    df.columns = df.columns.astype("str")
    return df
