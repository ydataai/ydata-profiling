import warnings

from ydata_profiling.model.dataframe import check_dataframe, preprocess
from ydata_profiling.model.modin import utils_modin
from ydata_profiling.model.pandas.dataframe_pandas import pandas_preprocess
from ydata_profiling.utils import modin


@check_dataframe.register
def modin_check_dataframe(df: modin.DataFrame) -> None:
    if not isinstance(df, modin.DataFrame):
        warnings.warn("df is not of type modin.DataFrame")


modin_preprocess = utils_modin.register(preprocess, pandas_preprocess)
