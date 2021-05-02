from functools import singledispatch
from typing import Tuple

import numpy as np
import pandas as pd

from pandas_profiling.model.dataframe_wrappers import SparkDataFrame
from pandas_profiling.model.summary_algorithms_pandas import (
    describe_boolean_1d_pandas,
    describe_categorical_1d_pandas,
    describe_counts_pandas,
    describe_date_1d_pandas,
    describe_file_1d_pandas,
    describe_generic_pandas,
    describe_image_1d_pandas,
    describe_numeric_1d_pandas,
    describe_path_1d_pandas,
    describe_supported_pandas,
    describe_url_1d_pandas,
    numeric_stats_numpy,
    numeric_stats_pandas,
)
from pandas_profiling.model.summary_algorithms_spark import (
    describe_boolean_1d_spark,
    describe_categorical_1d_spark,
    describe_counts_spark,
    describe_generic_spark,
    describe_numeric_1d_spark,
    describe_supported_spark,
    numeric_stats_spark,
)


@singledispatch
def describe_counts(series, summary: dict) -> Tuple[pd.Series, dict]:
    """Counts the values in a series (with and without NaN, distinct).

    Args:
        series: Series for which we want to calculate the values.

    Returns:
        A dictionary with the count values (with and without NaN, distinct).
    """
    raise NotImplementedError(f"Function not implemented for series type {series}")


describe_counts.register(pd.Series, describe_counts_pandas)
describe_counts.register(SparkDataFrame, describe_counts_spark)


@singledispatch
def describe_supported(series, series_description: dict) -> Tuple[pd.Series, dict]:
    """Describe a supported series.
    Args:
        series: The Series to describe.
        series_description: The dict containing the series description so far.
    Returns:
        A dict containing calculated series description values.
    """
    raise NotImplementedError(f"Function not implemented for series type {series}")


describe_supported.register(pd.Series, describe_supported_pandas)
describe_supported.register(SparkDataFrame, describe_supported_spark)


@singledispatch
def describe_generic(series, summary: dict) -> Tuple[pd.Series, dict]:
    """Describe generic series.
    Args:
        series: The Series to describe.
        summary: The dict containing the series description so far.
    Returns:
        A dict containing calculated series description values.
    """
    raise NotImplementedError(f"Function not implemented for series type {series}")


describe_generic.register(pd.Series, describe_generic_pandas)
describe_generic.register(SparkDataFrame, describe_generic_spark)


@singledispatch
def numeric_stats(series):
    raise NotImplementedError(f"Function not implemented for series type {series}")


numeric_stats.register(np.array, numeric_stats_numpy)
numeric_stats.register(pd.Series, numeric_stats_pandas)
numeric_stats.register(SparkDataFrame, numeric_stats_spark)


@singledispatch
def describe_numeric_1d(series, summary: dict) -> Tuple[pd.Series, dict]:
    """Describe a numeric series.
    Args:
        series: The Series to describe.
        summary: The dict containing the series description so far.
    Returns:
        A dict containing calculated series description values.
    """
    raise NotImplementedError(f"Function not implemented for series type {series}")


describe_numeric_1d.register(pd.Series, describe_numeric_1d_pandas)
describe_numeric_1d.register(SparkDataFrame, describe_numeric_1d_spark)


@singledispatch
def describe_date_1d(series, summary: dict) -> Tuple[pd.Series, dict]:
    """Describe a date series.

    Args:
        series: The Series to describe.
        summary: The dict containing the series description so far.

    Returns:
        A dict containing calculated series description values.
    """
    raise NotImplementedError(f"Function not implemented for series type {series}")


describe_date_1d.register(pd.Series, describe_date_1d_pandas)


@singledispatch
def describe_categorical_1d(series, summary: dict) -> Tuple[pd.Series, dict]:
    """Describe a categorical series.

    Args:
        series: The Series to describe.
        summary: The dict containing the series description so far.

    Returns:
        A dict containing calculated series description values.
    """
    raise NotImplementedError(f"Function not implemented for series type {series}")


describe_categorical_1d.register(pd.Series, describe_categorical_1d_pandas)
describe_categorical_1d.register(SparkDataFrame, describe_categorical_1d_spark)


@singledispatch
def describe_url_1d(series, summary: dict) -> Tuple[pd.Series, dict]:
    """Describe a url series.

    Args:
        series: The Series to describe.
        summary: The dict containing the series description so far.

    Returns:
        A dict containing calculated series description values.
    """
    raise NotImplementedError(f"Function not implemented for series type {series}")


describe_url_1d.register(pd.Series, describe_url_1d_pandas)


@singledispatch
def describe_file_1d(series, summary: dict) -> Tuple[pd.Series, dict]:
    raise NotImplementedError(f"Function not implemented for series type {series}")


describe_file_1d.register(pd.Series, describe_file_1d_pandas)


@singledispatch
def describe_path_1d(series, summary: dict) -> Tuple[pd.Series, dict]:
    """Describe a path series.

    Args:
        series: The Series to describe.
        summary: The dict containing the series description so far.

    Returns:
        A dict containing calculated series description values.
    """
    raise NotImplementedError(f"Function not implemented for series type {series}")


describe_path_1d.register(pd.Series, describe_path_1d_pandas)


@singledispatch
def describe_image_1d(series, summary: dict) -> Tuple[pd.Series, dict]:
    raise NotImplementedError(f"Function not implemented for series type {series}")


describe_image_1d.register(pd.Series, describe_image_1d_pandas)


@singledispatch
def describe_boolean_1d(series, summary: dict) -> Tuple[pd.Series, dict]:
    """Describe a boolean series.

    Args:
        series: The Series to describe.
        summary: The dict containing the series description so far.

    Returns:
        A dict containing calculated series description values.
    """
    raise NotImplementedError(f"Function not implemented for series type {series}")


describe_boolean_1d.register(pd.Series, describe_boolean_1d_pandas)
describe_boolean_1d.register(SparkDataFrame, describe_boolean_1d_spark)
