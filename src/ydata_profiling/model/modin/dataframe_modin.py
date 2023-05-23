import warnings

from ydata_profiling.config import Settings
from ydata_profiling.model.dataframe import check_dataframe, preprocess
from ydata_profiling.model.pandas.dataframe_pandas import pandas_preprocess
from ydata_profiling.utils import modin


@check_dataframe.register
def modin_check_dataframe(df: modin.DataFrame) -> None:
    if not isinstance(df, modin.DataFrame):
        warnings.warn("df is not of type modin.DataFrame")


@preprocess.register
def modin_preprocess(config: Settings, df: modin.DataFrame) -> modin.DataFrame:
    return pandas_preprocess(config, df)
