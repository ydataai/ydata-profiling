"""Compute statistical description of datasets."""
import multiprocessing.pool
import multiprocessing
import itertools
import os
import sys
import warnings
from pathlib import Path
from typing import Tuple
from urllib.parse import urlsplit

from tqdm.autonotebook import tqdm
import numpy as np
import pandas as pd
from astropy.stats import bayesian_blocks
from scipy.stats.stats import chisquare

from pandas_profiling import __version__
from pandas_profiling.config import config as config
from pandas_profiling.model.messages import (
    check_variable_messages,
    check_table_messages,
    warning_type_date,
    check_correlation_messages,
)

from pandas_profiling.model import base
from pandas_profiling.model.base import Variable
from pandas_profiling.model.correlations import calculate_correlations
from pandas_profiling.visualisation.missing import (
    missing_bar,
    missing_matrix,
    missing_heatmap,
    missing_dendrogram,
)
from pandas_profiling.visualisation.plot import scatter_pairwise


def describe_numeric_1d(series: pd.Series, series_description: dict) -> dict:
    """Describe a numeric series.

    Args:
        series: The Series to describe.
        series_description: The dict containing the series description so far.

    Returns:
        A dict containing calculated series description values.

    Notes:
        When 'bins_type' is set to 'bayesian_blocks', astropy.stats.bayesian_blocks is used to determine the number of
        bins. Read the docs:
        https://docs.astropy.org/en/stable/visualization/histogram.html
        https://docs.astropy.org/en/stable/api/astropy.stats.bayesian_blocks.html

        This method might print warnings, which we suppress.
        https://github.com/astropy/astropy/issues/4927
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
        "histogram_data": series,
        "scatter_data": series,  # For complex
    }

    chi_squared_threshold = config["vars"]["num"]["chi_squared_threshold"].get(float)
    if chi_squared_threshold > 0.0:
        histogram = np.histogram(series[series.notna()].values, bins="auto")[0]
        stats["chi_squared"] = chisquare(histogram)

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

    bins = config["plot"]["histogram"]["bins"].get(int)
    # Bins should never be larger than the number of distinct values
    bins = min(series_description["distinct_count_with_nan"], bins)
    stats["histogram_bins"] = bins

    bayesian_blocks_bins = config["plot"]["histogram"]["bayesian_blocks_bins"].get(bool)
    if bayesian_blocks_bins:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            ret = bayesian_blocks(stats["histogram_data"])

            # Sanity check
            if not np.isnan(ret).any() and ret.size > 1:
                stats["histogram_bins_bayesian_blocks"] = ret

    return stats


def describe_date_1d(series: pd.Series, series_description: dict) -> dict:
    """Describe a date series.

    Args:
        series: The Series to describe.
        series_description: The dict containing the series description so far.

    Returns:
        A dict containing calculated series description values.
    """
    stats = {"min": series.min(), "max": series.max(), "histogram_data": series}

    bins = config["plot"]["histogram"]["bins"].get(int)
    # Bins should never be larger than the number of distinct values
    bins = min(series_description["distinct_count_with_nan"], bins)
    stats["histogram_bins"] = bins

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
    # Make sure we deal with strings (Issue #100)
    series = series.astype(str)

    # Only run if at least 1 non-missing value
    value_counts = series_description["value_counts_without_nan"]

    stats = {"top": value_counts.index[0], "freq": value_counts.iloc[0]}

    chi_squared_threshold = config["vars"]["num"]["chi_squared_threshold"].get(float)
    if chi_squared_threshold > 0.0:
        stats["chi_squared"] = list(chisquare(value_counts.values))

    check_composition = config["vars"]["cat"]["check_composition"].get(bool)
    if check_composition:
        stats["max_length"] = series.str.len().max()
        stats["mean_length"] = series.str.len().mean()
        stats["min_length"] = series.str.len().min()

        from visions.application.summaries.series.text_summary import text_summary

        stats.update(text_summary(series))
        stats["length"] = series.str.len()

    stats["date_warning"] = warning_type_date(series)

    return stats


def describe_url_1d(series: pd.Series, series_description: dict) -> dict:
    """Describe a url series.

    Args:
        series: The Series to describe.
        series_description: The dict containing the series description so far.

    Returns:
        A dict containing calculated series description values.
    """
    # Make sure we deal with strings (Issue #100)
    series = series[~series.isnull()].astype(str)

    stats = {}

    # Create separate columns for each URL part
    keys = ["scheme", "netloc", "path", "query", "fragment"]
    url_parts = dict(zip(keys, zip(*series.map(urlsplit))))
    for name, part in url_parts.items():
        stats["{}_counts".format(name.lower())] = pd.Series(
            part, name=name
        ).value_counts()

    # Only run if at least 1 non-missing value
    value_counts = series_description["value_counts_without_nan"]

    stats["top"] = value_counts.index[0]
    stats["freq"] = value_counts.iloc[0]

    return stats


def describe_path_1d(series: pd.Series, series_description: dict) -> dict:
    """Describe a path series.

    Args:
        series: The Series to describe.
        series_description: The dict containing the series description so far.

    Returns:
        A dict containing calculated series description values.
    """
    series_description.update(describe_categorical_1d(series, series_description))

    # Make sure we deal with strings (Issue #100)
    series = series[~series.isnull()].astype(str)
    series = series.map(Path)

    common_prefix = os.path.commonprefix(list(series))
    if common_prefix == "":
        common_prefix = "No common prefix"

    stats = {"common_prefix": common_prefix}

    # Create separate columns for each path part
    keys = ["stem", "suffix", "name", "parent"]
    path_parts = dict(
        zip(keys, zip(*series.map(lambda x: [x.stem, x.suffix, x.name, x.parent])))
    )
    for name, part in path_parts.items():
        stats["{}_counts".format(name.lower())] = pd.Series(
            part, name=name
        ).value_counts()

    # Only run if at least 1 non-missing value
    value_counts = series_description["value_counts_without_nan"]

    stats["top"] = value_counts.index[0]
    stats["freq"] = value_counts.iloc[0]

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
        "n": leng,
        "count": count,
        "distinct_count": distinct_count,
        "n_unique": distinct_count,
        "p_missing": 1 - count * 1.0 / leng,
        "n_missing": leng - count,
        "p_infinite": n_infinite * 1.0 / leng,
        "n_infinite": n_infinite,
        "is_unique": distinct_count == leng,
        "mode": series.mode().iloc[0] if count > distinct_count > 1 else series[0],
        "p_unique": distinct_count * 1.0 / leng,
        "memory_size": series.memory_usage(),
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
        "n": leng,
        "count": count,
        "p_missing": 1 - count * 1.0 / leng,
        "n_missing": leng - count,
        "p_infinite": n_infinite * 1.0 / leng,
        "n_infinite": n_infinite,
        "memory_size": series.memory_usage(),
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
            Variable.TYPE_BOOL: describe_boolean_1d,
            Variable.TYPE_NUM: describe_numeric_1d,
            Variable.TYPE_DATE: describe_date_1d,
            Variable.TYPE_CAT: describe_categorical_1d,
            Variable.TYPE_URL: describe_url_1d,
            Variable.TYPE_PATH: describe_path_1d,
        }

        if series_description["type"] in type_to_func:
            series_description.update(
                type_to_func[series_description["type"]](series, series_description)
            )
        else:
            raise ValueError("Unexpected type")

    # Return the description obtained
    return series_description


def multiprocess_1d(args) -> Tuple[str, dict]:
    """Wrapper to process series in parallel.

    Args:
        column: The name of the column.
        series: The series values.

    Returns:
        A tuple with column and the series description.
    """
    column, series = args
    return column, describe_1d(series)


def describe_table(df: pd.DataFrame, variable_stats: pd.DataFrame) -> dict:
    """General statistics for the DataFrame.

    Args:
      df: The DataFrame to describe.
      variable_stats: Previously calculated statistic on the DataFrame.

    Returns:
        A dictionary that contains the table statistics.
    """
    n = len(df)

    memory_size = df.memory_usage(index=True, deep=True).sum()
    record_size = float(memory_size) / n

    table_stats = {
        "n": n,
        "n_var": len(df.columns),
        "memory_size": memory_size,
        "record_size": record_size,
        "n_cells_missing": variable_stats.loc["n_missing"].sum(),
        "n_vars_with_missing": sum((variable_stats.loc["n_missing"] > 0).astype(int)),
        "n_vars_all_missing": sum((variable_stats.loc["n_missing"] == n).astype(int)),
    }

    table_stats["p_cells_missing"] = table_stats["n_cells_missing"] / (
        table_stats["n"] * table_stats["n_var"]
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
        {
            "types": dict(
                variable_stats.loc["type"].apply(lambda x: x.value).value_counts()
            )
        }
    )

    return table_stats


def warn_missing(missing_name, error):
    warnings.warn(
        "There was an attempt to generate the {missing_name} missing values diagrams, but this failed.\n"
        "To hide this warning, disable the calculation\n"
        '(using `df.profile_report(missing_diagrams={{"{missing_name}": False}}`)\n'
        "If this is problematic for your use case, please report this as an issue:\n"
        "https://github.com/pandas-profiling/pandas-profiling/issues\n"
        "(include the error message: '{error}')".format(
            missing_name=missing_name, error=error
        )
    )


def get_missing_diagrams(df: pd.DataFrame, table_stats: dict) -> dict:
    """Gets the rendered diagrams for missing values.

    Args:
        table_stats: The overall statistics for the DataFrame.
        df: The DataFrame on which to calculate the missing values.

    Returns:
        A dictionary containing the base64 encoded plots for each diagram that is active in the config (matrix, bar, heatmap, dendrogram).
    """
    disable_progress_bar = not config["progress_bar"].get(bool)

    missing_map = {
        "bar": {"func": missing_bar, "min_missing": 0, "name": "Count"},
        "matrix": {"func": missing_matrix, "min_missing": 0, "name": "Matrix"},
        "heatmap": {"func": missing_heatmap, "min_missing": 2, "name": "Heatmap"},
        "dendrogram": {
            "func": missing_dendrogram,
            "min_missing": 1,
            "name": "Dendrogram",
        },
    }

    with tqdm(
        total=len(missing_map), desc="missing", disable=disable_progress_bar
    ) as pbar:
        missing = {}
        for name, settings in missing_map.items():
            pbar.set_description_str("missing [{name}]".format(name=name))
            if (
                config["missing_diagrams"][name].get(bool)
                and table_stats["n_vars_with_missing"] >= settings["min_missing"]
            ):
                try:
                    if name != "heatmap" or (
                        table_stats["n_vars_with_missing"]
                        - table_stats["n_vars_all_missing"]
                        >= settings["min_missing"]
                    ):
                        missing[name] = {
                            "name": settings["name"],
                            "matrix": settings["func"](df),
                        }
                except ValueError as e:
                    warn_missing(name, e)
            pbar.update()
    return missing


def get_scatter_matrix(df, variables):
    disable_progress_bar = not config["progress_bar"].get(bool)

    if config["interactions"]["continuous"].get(bool):
        continuous_variables = [
            column for column, type in variables.items() if type == Variable.TYPE_NUM
        ]
        with tqdm(
            total=len(continuous_variables) ** 2,
            desc="interactions [continuous]",
            disable=disable_progress_bar,
        ) as pbar:
            scatter_matrix = {
                x: {y: "" for y in continuous_variables} for x in continuous_variables
            }
            for x in continuous_variables:
                for y in continuous_variables:
                    scatter_matrix[x][y] = scatter_pairwise(df[x], df[y], x, y)
                    pbar.update()
    else:
        scatter_matrix = {}

    return scatter_matrix


def sort_column_names(dct):
    sort = config["sort"].get(str)
    if sys.version_info[1] <= 5 and sort != "None":
        warnings.warn("Sorting is supported from Python 3.6+")
    else:
        if sort in ["asc", "ascending"]:
            dct = dict(sorted(dct.items(), key=lambda x: x[0].casefold()))
        elif sort in ["desc", "descending"]:
            dct = dict(reversed(sorted(dct.items(), key=lambda x: x[0].casefold())))
        elif sort != "None":
            raise ValueError('"sort" should be "ascending", "descending" or None.')
    return dct


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

    disable_progress_bar = not config["progress_bar"].get(bool)

    # Multiprocessing of Describe 1D for each column
    pool_size = config["pool_size"].get(int)
    if pool_size <= 0:
        pool_size = multiprocessing.cpu_count()

    args = [(column, series) for column, series in df.iteritems()]
    series_description = {}
    with tqdm(total=len(args), desc="variables", disable=disable_progress_bar) as pbar:
        if pool_size == 1:
            for arg in args:
                column, description = multiprocess_1d(arg)
                series_description[column] = description
                pbar.update(1)
        else:
            with multiprocessing.pool.ThreadPool(pool_size) as executor:
                for i, (column, description) in enumerate(
                    executor.imap_unordered(multiprocess_1d, args)
                ):
                    series_description[column] = description
                    pbar.update(1)

    # Mapping from column name to variable type
    series_description = sort_column_names(series_description)

    variables = {
        column: description["type"]
        for column, description in series_description.items()
    }

    # Transform the series_description in a DataFrame
    variable_stats = pd.DataFrame(series_description)

    # Get correlations
    correlations = calculate_correlations(df, variables)

    # Scatter matrix
    scatter_matrix = get_scatter_matrix(df, variables)

    # Table statistics
    with tqdm(total=1, desc="table", disable=disable_progress_bar) as pbar:
        table_stats = describe_table(df, variable_stats)
        pbar.update(1)

    # missing diagrams
    missing = get_missing_diagrams(df, table_stats)

    # Messages
    with tqdm(total=3, desc="warnings", disable=disable_progress_bar) as pbar:
        pbar.set_description_str("warnings [table]")
        messages = check_table_messages(table_stats)
        pbar.update(1)
        pbar.set_description_str("warnings [variables]")
        for col, description in series_description.items():
            messages += check_variable_messages(col, description)
        pbar.update(1)
        pbar.set_description_str("warnings [correlations]")
        messages += check_correlation_messages(correlations)
        pbar.update(1)

    with tqdm(total=1, desc="package", disable=disable_progress_bar) as pbar:
        package = {
            "pandas_profiling_version": __version__,
            "pandas_profiling_config": config.dump(),
        }
        pbar.update(1)

    return {
        # Overall description
        "table": table_stats,
        # Per variable descriptions
        "variables": series_description,
        # Bivariate relations
        "scatter": scatter_matrix,
        # Correlation matrices
        "correlations": correlations,
        # Missing values
        "missing": missing,
        # Warnings
        "messages": messages,
        # Package
        "package": package,
    }
