"""Compute statistical description of datasets."""
import importlib
from typing import Any

import pandas as pd
from tqdm import tqdm
from visions import VisionsTypeset

from ydata_profiling.config import Settings
from ydata_profiling.model.pandas.summary_pandas import (
    pandas_describe_1d,
    pandas_get_series_descriptions,
)
from ydata_profiling.model.summarizer import BaseSummarizer

spec = importlib.util.find_spec("pyspark")
if spec is None:
    from typing import TypeVar  # noqa: E402

    sparkDataFrame = TypeVar("sparkDataFrame")  # type: ignore
    sparkSeries = TypeVar("sparkSeries")  # type: ignore
else:
    from pyspark.sql import DataFrame as sparkDataFrame  # type: ignore

    from ydata_profiling.model.spark.summary_spark import (  # noqa: E402
        get_series_descriptions_spark,
        spark_describe_1d,
    )


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
    elif isinstance(series, sparkDataFrame):  # type: ignore
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
    elif isinstance(df, sparkDataFrame):  # type: ignore
        return get_series_descriptions_spark(config, df, summarizer, typeset, pbar)
    else:
        raise TypeError(f"Unsupported dataframe type: {type(df)}")
