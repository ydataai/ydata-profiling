import warnings

from pyspark.sql import DataFrame

from pandas_profiling.config import Settings
from pandas_profiling.model.dataframe import check_dataframe, preprocess


@check_dataframe.register
def spark_check_dataframe(df: DataFrame) -> None:
    # FIXME: never...
    if not isinstance(df, DataFrame):
        warnings.warn("df is not of type pyspark.sql.dataframe.DataFrame")


@preprocess.register
def spark_preprocess(config: Settings, df: DataFrame) -> DataFrame:
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
    # Treat index as any other column
    # if (
    #     not pd.Index(np.arange(0, len(df))).equals(df.index)
    #     or df.index.dtype != np.int64
    # ):
    #     df = df.reset_index()
    #
    # # Rename reserved column names
    # df = rename_index(df)
    #
    # # Ensure that columns are strings
    # df.columns = df.columns.astype("str")

    if config.persist:
        # persist dataframe to improve speed
        df.persist()

    return df
