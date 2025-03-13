import importlib
from typing import Any

import pandas as pd

spec = importlib.util.find_spec("pyspark")
if spec is None:
    from typing import TypeVar

    sparkDataFrame = TypeVar("sparkDataFrame")
else:
    from pyspark.sql import DataFrame as sparkDataFrame
    from ydata_profiling.model.spark.dataframe_spark import spark_preprocess

from ydata_profiling.config import Settings
from ydata_profiling.model.pandas.dataframe_pandas import pandas_preprocess


def preprocess(config: Settings, df: Any) -> Any:
    """
    Search for invalid columns datatypes as well as ensures column names follow the expected rules
    Args:
        config: ydataprofiling Settings class
        df: a pandas or spark dataframe

    Returns: a pandas or spark dataframe
    """
    if isinstance(df, pd.DataFrame):
        df = pandas_preprocess(config=config, df=df)
    elif isinstance(df, sparkDataFrame):
        df = spark_preprocess(config=config, df=df)
    else:
        return NotImplementedError()
    return df
