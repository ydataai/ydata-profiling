"""Compute statistical description of datasets."""

from functools import singledispatch

import pandas as pd

from pandas_profiling.model.dataframe_wrappers import (
    GenericDataFrame,
    PandasDataFrame,
    SparkDataFrame,
)
from pandas_profiling.model.summarizer import BaseSummarizer
from pandas_profiling.model.summary_pandas import (
    describe_1d_pandas,
    get_missing_diagrams_pandas,
    get_scatter_matrix_pandas,
    get_series_descriptions_pandas,
    get_table_stats_pandas,
)
from pandas_profiling.model.summary_spark import (
    get_missing_diagrams_spark,
    get_scatter_matrix_spark,
    get_series_descriptions_spark,
    get_table_stats_spark,
)


@singledispatch
def describe_1d(series, summarizer: BaseSummarizer, typeset) -> dict:
    """Describe a series (infer the variable type, then calculate type-specific values).

    Args:
        series: The Series to describe.

    Returns:
        A Series containing calculated series description values.
    """
    raise NotImplementedError("Method is not implemented for dtype")


describe_1d.register(pd.Series, describe_1d_pandas)


@singledispatch
def get_series_descriptions(df: GenericDataFrame, summarizer, typeset, pbar):
    raise NotImplementedError(
        f"get_table_stats is not implemented for datatype {type(df)}"
    )


get_series_descriptions.register(PandasDataFrame, get_series_descriptions_pandas)
get_series_descriptions.register(SparkDataFrame, get_series_descriptions_spark)


@singledispatch
def get_table_stats(df: GenericDataFrame, variable_stats: dict) -> dict:
    """General statistics for the DataFrame.

    Args:
      df: The DataFrame to describe.
      variable_stats: Previously calculated statistic on the DataFrame.

    Returns:
        A dictionary that contains the table statistics.
    """
    raise NotImplementedError(
        f"get_table_stats is not implemented for datatype {type(df)}"
    )


get_table_stats.register(PandasDataFrame, get_table_stats_pandas)
get_table_stats.register(SparkDataFrame, get_table_stats_spark)


@singledispatch
def get_missing_diagrams(df: GenericDataFrame, table_stats: dict) -> dict:
    """Gets the rendered diagrams for missing values.

    Args:
        table_stats: The overall statistics for the DataFrame.
        df: The DataFrame on which to calculate the missing values.

    Returns:
        A dictionary containing the base64 encoded plots for each diagram that is active in the config (matrix, bar, heatmap, dendrogram).
    """
    raise NotImplementedError(
        f"get_missing_diagrams is not implemented for datatype {type(df)}"
    )


get_missing_diagrams.register(PandasDataFrame, get_missing_diagrams_pandas)
get_missing_diagrams.register(SparkDataFrame, get_missing_diagrams_spark)


@singledispatch
def get_scatter_matrix(df: GenericDataFrame, continuous_variables):
    raise NotImplementedError(
        f"get_table_stats is not implemented for datatype {type(df)}"
    )


get_scatter_matrix.register(PandasDataFrame, get_scatter_matrix_pandas)
get_scatter_matrix.register(SparkDataFrame, get_scatter_matrix_spark)
