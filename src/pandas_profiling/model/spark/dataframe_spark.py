import warnings

from pyspark.sql import DataFrame
from pyspark.sql.functions import array, map_keys, map_values
from pyspark.sql.types import MapType

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

    # this converts any MapTypes into ArrayType as MapTypes cannot be groupby-ed
    column_type_tuple = list(zip(df.columns, [i.dataType for i in df.schema]))
    converted_dataframe = df
    for column, col_type in column_type_tuple:
        if isinstance(col_type, MapType):
            converted_dataframe = converted_dataframe.withColumn(
                column,
                array(
                    map_keys(converted_dataframe[column]),
                    map_values(converted_dataframe[column]),
                ),
            )

    return converted_dataframe
