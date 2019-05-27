"""Compute statistical description of datasets."""
import multiprocessing.pool
import multiprocessing
import itertools
from typing import Tuple

import numpy as np
import pandas as pd

from pandas_profiling.config import config as config
from pandas_profiling.model.messages import (
    check_variable_messages,
    check_table_messages,
)

import pandas_profiling.view.formatters as formatters
from pandas_profiling.model import base
from pandas_profiling.model.base import Variable
from pandas_profiling.model.correlations import (
    calculate_correlations,
    perform_check_correlation,
    perform_check_recoded,
)
from pandas_profiling.view import plot


def describe_numeric_1d(series: pd.Series, series_description: dict) -> dict:
    """Describe a numeric series.

    Args:
        series: The Series to describe.
        series_description: The dict containing the series description so far.

    Returns:
        A dict containing calculated series description values.
    """
    quantiles = config["vars"]["num"]["quantiles"].get(list)

    stats = {
        "mean": series.mean(),
        "std": series.std(),
        "variance": series.var(),
        "min": series.min(),
        "max": series.max(),
        "kurtosis": series.kurt(),
        "skewness": series.skew(),
        "sum": series.sum(),
        "mad": series.mad(),
        "n_zeros": (len(series) - np.count_nonzero(series)),
        "histogramdata": series,
    }

    stats["range"] = stats["max"] - stats["min"]
    stats.update(
        {
            "{:.0%}".format(percentile): value
            for percentile, value in series.quantile(quantiles).to_dict().items()
        }
    )
    stats["iqr"] = stats["75%"] - stats["25%"]
    stats["cv"] = stats["std"] / stats["mean"] if stats["mean"] else np.NaN
    stats["p_zeros"] = float(stats["n_zeros"]) / len(series)

    return stats


def describe_date_1d(series: pd.Series, series_description: dict) -> dict:
    """Describe a date series.

    Args:
        series: The Series to describe.
        series_description: The dict containing the series description so far.

    Returns:
        A dict containing calculated series description values.
    """
    stats = {
        "min": series.min(),
        "max": series.max(),
        "histogramdata": series,  # TODO: calc histogram here?
    }

    stats["range"] = stats["max"] - stats["min"]

    return stats


def describe_categorical_1d(series: pd.Series, series_description: dict) -> dict:
    """Describe a categorical series.

    Args:
        series: The Series to describe.
        series_description: The dict containing the series description so far.

    Returns:
        A dict containing calculated series description values.
    """

    # Only run if at least 1 non-missing value
    value_counts = series_description["value_counts_without_nan"]

    stats = {"top": value_counts.index[0], "freq": value_counts.iloc[0]}

    check_composition = config["vars"]["cat"]["check_composition"].get(bool)
    if check_composition:
        contains = {
            "chars": series.str.contains(r"[a-zA-Z]", case=False, regex=True).any(),
            "digits": series.str.contains(r"[0-9]", case=False, regex=True).any(),
            "spaces": series.str.contains(r"\s", case=False, regex=True).any(),
            "non-words": series.str.contains(r"\W", case=False, regex=True).any(),
        }
        stats["max_length"] = series.str.len().max()
        stats["mean_length"] = series.str.len().mean()
        stats["min_length"] = series.str.len().min()
        stats["composition"] = contains

    return stats


def describe_boolean_1d(series: pd.Series, series_description: dict) -> dict:
    """Describe a boolean series.

    Args:
        series: The Series to describe.
        series_description: The dict containing the series description so far.

    Returns:
        A dict containing calculated series description values.
    """
    value_counts = series_description["value_counts_without_nan"]

    stats = {"top": value_counts.index[0], "freq": value_counts.iloc[0]}

    return stats


def describe_constant_1d(series: pd.Series, series_description: dict) -> dict:
    """Describe a constant series (placeholder).

    Args:
        series: The Series to describe.
        series_description: The dict containing the series description so far.

    Returns:
        An empty dict.
    """
    return {}


def describe_unique_1d(series: pd.Series, series_description: dict) -> dict:
    """Describe a unique series (placeholder).

    Args:
        series: The Series to describe.
        series_description: The dict containing the series description so far.

    Returns:
        An empty dict.
    """
    return {}


def describe_supported(series: pd.Series, series_description: dict) -> dict:
    """Describe a supported series.

    Args:
        series: The Series to describe.
        series_description: The dict containing the series description so far.

    Returns:
        A dict containing calculated series description values.
    """

    # number of observations in the Series
    leng = len(series)
    # TODO: fix infinite logic
    # number of non-NaN observations in the Series
    count = series.count()
    # number of infinite observations in the Series
    n_infinite = count - series.count()

    # TODO: check if we prefer without nan
    distinct_count = series_description["distinct_count_with_nan"]

    stats = {
        "count": count,
        "distinct_count": distinct_count,
        "p_missing": 1 - count * 1.0 / leng,
        "n_missing": leng - count,
        "p_infinite": n_infinite * 1.0 / leng,
        "n_infinite": n_infinite,
        "is_unique": distinct_count == leng,
        "mode": series.mode().iloc[0] if count > distinct_count > 1 else series[0],
        "p_unique": distinct_count * 1.0 / leng,
        "memorysize": series.memory_usage(),
    }

    return stats


def describe_unsupported(series: pd.Series, series_description: dict):
    """Describe an unsupported series.

    Args:
        series: The Series to describe.
        series_description: The dict containing the series description so far.

    Returns:
        A dict containing calculated series description values.
    """

    # number of observations in the Series
    leng = len(series)
    # number of non-NaN observations in the Series
    count = series.count()
    # number of infinte observations in the Series
    n_infinite = count - series.count()

    results_data = {
        "count": count,
        "p_missing": 1 - count * 1.0 / leng,
        "n_missing": leng - count,
        "p_infinite": n_infinite * 1.0 / leng,
        "n_infinite": n_infinite,
        "memorysize": series.memory_usage(),
    }

    return results_data


def describe_1d(series: pd.Series) -> dict:
    """Describe a series (infer the variable type, then calculate type-specific values).

    Args:
        series: The Series to describe.

    Returns:
        A Series containing calculated series description values.
    """

    # Replace infinite values with NaNs to avoid issues with histograms later.
    series.replace(to_replace=[np.inf, np.NINF, np.PINF], value=np.nan, inplace=True)

    # Infer variable types
    series_description = base.get_var_type(series)

    # Run type specific analysis
    if series_description["type"] == Variable.S_TYPE_UNSUPPORTED:
        series_description.update(describe_unsupported(series, series_description))
    else:
        series_description.update(describe_supported(series, series_description))

        type_to_func = {
            Variable.S_TYPE_CONST: describe_constant_1d,
            Variable.TYPE_BOOL: describe_boolean_1d,
            Variable.TYPE_NUM: describe_numeric_1d,
            Variable.TYPE_DATE: describe_date_1d,
            Variable.S_TYPE_UNIQUE: describe_unique_1d,
            Variable.TYPE_CAT: describe_categorical_1d,
        }

        if series_description["type"] in type_to_func:
            series_description.update(
                type_to_func[series_description["type"]](series, series_description)
            )
        else:
            raise ValueError("Unexpected type")

    # Return the description obtained
    return series_description


def multiprocess_1d(column, series) -> Tuple[str, dict]:
    """Wrapper to process series in parallel.

    Args:
        column: The name of the column.
        series: The series values.

    Returns:
        A tuple with column and the series description.
    """
    return column, describe_1d(series)


def describe_table(df: pd.DataFrame, variable_stats: pd.DataFrame) -> dict:
    """General statistics for the DataFrame.

    Args:
      df: The DataFrame to describe.
      variable_stats: Previously calculated statistic on the DataFrame.

    Returns:
        A dictionary containg the table statistics.
    """
    n = len(df)
    memory_size = df.memory_usage(index=True).sum()
    record_size = float(memory_size) / n

    table_stats = {
        "n": n,
        "nvar": len(df.columns),
        "memsize": formatters.fmt_bytesize(memory_size),
        "recordsize": formatters.fmt_bytesize(record_size),
        "n_cells_missing": variable_stats.loc["n_missing"].sum(),
    }

    table_stats["p_cells_missing"] = table_stats["n_cells_missing"] / (
        table_stats["n"] * table_stats["nvar"]
    )

    supported_columns = variable_stats.transpose()[
        variable_stats.transpose().type != Variable.S_TYPE_UNSUPPORTED
    ].index.tolist()
    table_stats["n_duplicates"] = (
        sum(df.duplicated(subset=supported_columns))
        if len(supported_columns) > 0
        else 0
    )
    table_stats["p_duplicates"] = (
        (table_stats["n_duplicates"] / len(df))
        if (len(supported_columns) > 0 and len(df) > 0)
        else 0
    )

    # Variable type counts
    table_stats.update({k.value: 0 for k in Variable})
    table_stats.update(
        dict(variable_stats.loc["type"].apply(lambda x: x.value).value_counts())
    )
    table_stats[Variable.S_TYPE_REJECTED.value] = (
        table_stats[Variable.S_TYPE_CONST.value]
        + table_stats[Variable.S_TYPE_CORR.value]
        + table_stats[Variable.S_TYPE_RECODED.value]
    )
    return table_stats


def get_missing_diagrams(df: pd.DataFrame):
    """Gets the rendered diagrams for missing values.

    Args:
        df: The DataFrame on which to calculate the missing values.

    Returns:
        A dictionary containing the base64 encoded plots for each diagram that is active in the config (matrix, bar, heatmap, dendrogram).
    """
    missing_map = {
        "matrix": plot.missing_matrix,
        "bar": plot.missing_bar,
        "heatmap": plot.missing_heatmap,
        "dendrogram": plot.missing_dendrogram,
    }

    missing = {}
    for name, func in missing_map.items():
        if config["missing_diagrams"][name].get(bool):
            missing[name] = func(df)
    return missing


def describe(df: pd.DataFrame) -> dict:
    """Calculate the statistics for each series in this DataFrame.

    Args:
        df: DataFrame.

    Returns:
        This function returns a dictionary containing:
            - table: overall statistics.
            - variables: descriptions per series.
            - correlations: correlation matrices.
            - missing: missing value diagrams.
            - messages: direct special attention to these patterns in your data.
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError("df must be of type pandas.DataFrame")

    if df.empty:
        raise ValueError("df can not be empty")

    # Treat index as any other column
    if not pd.Index(np.arange(0, len(df))).equals(df.index):
        df = df.reset_index()

    # Multiprocessing of Describe 1D for each column
    pool_size = config["pool_size"].get(int)
    if pool_size <= 0:
        pool_size = multiprocessing.cpu_count()

    if pool_size == 1:
        args = [(column, series) for column, series in df.iteritems()]
        series_description = {
            column: series
            for column, series in itertools.starmap(multiprocess_1d, args)
        }
    else:
        with multiprocessing.pool.ThreadPool(pool_size) as executor:
            series_description = {}
            results = executor.starmap(multiprocess_1d, df.iteritems())
            for col, description in results:
                series_description[col] = description

    variables = {
        column: description["type"]
        for column, description in series_description.items()
    }

    # Get correlations
    correlations = calculate_correlations(df)

    # Check correlations between variable
    if config["check_correlation"].get(bool) is True and "pearson" in correlations:
        # Overwrites the description with "CORR" series
        series_description.update(perform_check_correlation(correlations["pearson"]))

    # Check recoded
    if config["check_recoded"].get(bool) is True:
        # Overwrites the description with "RECORDED" series
        series_description.update(perform_check_recoded(df, variables))

    # Transform the series_description in a DataFrame
    variable_stats = pd.DataFrame(series_description)

    # Table statistics
    table_stats = describe_table(df, variable_stats)

    # missing diagrams
    missing = get_missing_diagrams(df)

    # Messages
    messages = check_table_messages(table_stats)
    for col, description in series_description.items():
        messages += check_variable_messages(col, description)

    return {
        # Overall desription
        "table": table_stats,
        # Per variable descriptions
        "variables": series_description,
        # Correlation matrices
        "correlations": correlations,
        # Missing values
        "missing": missing,
        # Warnings
        "messages": messages,
    }
