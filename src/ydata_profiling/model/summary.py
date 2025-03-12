"""Compute statistical description of datasets."""
import importlib
from typing import Any

from tqdm import tqdm
from visions import VisionsTypeset

import pandas as pd

spec = importlib.util.find_spec('pyspark')
if spec is None:
    from typing import TypeVar
    sparkDataFrame = TypeVar("sparkDataFrame")
    sparkDataFrame = TypeVar("sparkSeries")
else:
    from pyspark.sql import DataFrame as sparkDataFrame
    from pyspark.pandas import Series as sparkSeries

    from ydata_profiling.model.spark.summary_spark import spark_get_series_descriptions, spark_describe_1d


from ydata_profiling.config import Settings
from ydata_profiling.model.summarizer import BaseSummarizer

from ydata_profiling.model.pandas.summary_pandas import pandas_get_series_descriptions, pandas_describe_1d

# If could be doing this with a mapping instead?

def describe_1d(
    config: Settings,
    series: Any,
    summarizer: BaseSummarizer,
    typeset: VisionsTypeset,
) -> dict:
    """
    Add here the description and improve the documentation
    Args:
        config:
        series:
        summarizer:
        typeset:
    Returns:
    """
    if isinstance(series, pd.Series):
        return pandas_describe_1d(config, series, summarizer, typeset)
    elif isinstance(series, pd.DataFrame): #add here to validate the spark dataframe
        return spark_describe_1d(config, series, summarizer, typeset)
    else:
        raise TypeError(f"Unsupported series type: {type(series)}")

def get_series_descriptions(
    config: Settings,
    df: Any,
    summarizer: BaseSummarizer,
    typeset: VisionsTypeset,
    pbar: tqdm,
) -> dict:
    if isinstance(df, pd.DataFrame):
        return pandas_get_series_descriptions(config, df, summarizer, typeset, pbar)
    elif isinstance(df, sparkDataFrame):
        return spark_get_series_descriptions(config, df, summarizer, typeset, pbar)
    else:
        raise TypeError(f"Unsupported dataframe type: {type(df)}")
