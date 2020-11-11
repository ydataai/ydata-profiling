"""Compute statistical description of datasets."""

import multiprocessing
import multiprocessing.pool
import warnings
from pathlib import Path
from typing import Callable, Mapping, Optional, Tuple
from urllib.parse import urlsplit

import numpy as np
import pandas as pd
from pandas.core.arrays.integer import _IntegerDtype
from scipy.stats.stats import chisquare
from visions.application.summaries.series import (
    file_summary,
    image_summary,
    path_summary,
    url_summary,
)
from visions.application.summaries.series.text_summary import (
    length_summary,
    unicode_summary,
)

from pandas_profiling.config import config as config
from pandas_profiling.model import base
from pandas_profiling.model.base import Variable
from pandas_profiling.model.messages import (
    check_correlation_messages,
    check_table_messages,
    check_variable_messages,
    warning_type_date,
)
from pandas_profiling.visualisation.missing import (
    missing_bar,
    missing_bar2,
    missing_dendrogram,
    missing_heatmap,
    missing_matrix,
)
from pandas_profiling.visualisation.plot import scatter_pairwise


def sort_column_names(dct: Mapping, sort: str):
    sort = sort.lower()
    if sort.startswith("asc"):
        dct = dict(sorted(dct.items(), key=lambda x: x[0].casefold()))
    elif sort.startswith("desc"):
        dct = dict(reversed(sorted(dct.items(), key=lambda x: x[0].casefold())))
    elif sort != "none":
        raise ValueError('"sort" should be "ascending", "descending" or "None".')
    return dct


def describe_1d(series: pd.Series) -> dict:
    """Describe a series (infer the variable type, then calculate type-specific values).

    Args:
        series: The Series to describe.

    Returns:
        A Series containing calculated series description values.
    """

    def describe_supported(series: pd.Series, series_description: dict) -> dict:
        """Describe a supported series.
        Args:
            series: The Series to describe.
            series_description: The dict containing the series description so far.
        Returns:
            A dict containing calculated series description values.
        """

        # number of observations in the Series
        length = len(series)

        # number of non-NaN observations in the Series
        count = series.count()

        distinct_count = series_description["distinct_count_without_nan"]
        value_counts = series_description["value_counts_without_nan"]
        unique_count = value_counts.where(value_counts == 1).count()

        stats = {
            "n": length,
            "count": count,
            "n_distinct": distinct_count,
            "p_distinct": distinct_count / count,
            "p_missing": 1 - (count / length),
            "n_missing": length - count,
            "is_unique": unique_count == count,
            "n_unique": unique_count,
            "p_unique": unique_count / count,
            "memory_size": series.memory_usage(config["memory_deep"].get(bool)),
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
        length = len(series)

        # number of non-NaN observations in the Series
        count = series.count()

        results_data = {
            "n": length,
            "count": count,
            "p_missing": 1 - count / length,
            "n_missing": length - count,
            "memory_size": series.memory_usage(deep=config["memory_deep"].get(bool)),
        }

        return results_data

    def histogram_compute(finite_values, n_unique, name="histogram"):
        stats = {}
        bins = config["plot"]["histogram"]["bins"].get(int)
        bins = "auto" if bins == 0 else min(bins, n_unique)
        stats[name] = np.histogram(finite_values, bins)

        max_bins = config["plot"]["histogram"]["max_bins"].get(int)
        if bins == "auto" and len(stats[name][1]) > max_bins:
            stats[name] = np.histogram(finite_values, max_bins)

        return stats

    def numeric_stats_pandas(series: pd.Series):
        return {
            "mean": series.mean(),
            "std": series.std(),
            "variance": series.var(),
            "min": series.min(),
            "max": series.max(),
            # Unbiased kurtosis obtained using Fisher's definition (kurtosis of normal == 0.0). Normalized by N-1.
            "kurtosis": series.kurt(),
            # Unbiased skew normalized by N-1
            "skewness": series.skew(),
            "sum": series.sum(),
        }

    def numeric_stats_numpy(present_values):
        return {
            "mean": np.mean(present_values),
            "std": np.std(present_values, ddof=1),
            "variance": np.var(present_values, ddof=1),
            "min": np.min(present_values),
            "max": np.max(present_values),
            # Unbiased kurtosis obtained using Fisher's definition (kurtosis of normal == 0.0). Normalized by N-1.
            "kurtosis": series.kurt(),
            # Unbiased skew normalized by N-1
            "skewness": series.skew(),
            "sum": np.sum(present_values),
            "n_zeros": (series_description["count"] - np.count_nonzero(present_values)),
        }

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

        def mad(arr):
            """Median Absolute Deviation: a "Robust" version of standard deviation.
            Indices variability of the sample.
            https://en.wikipedia.org/wiki/Median_absolute_deviation
            """
            return np.median(np.abs(arr - np.median(arr)))

        quantiles = config["vars"]["num"]["quantiles"].get(list)

        n_infinite = ((series == np.inf) | (series == -np.inf)).sum()

        if isinstance(series.dtype, _IntegerDtype):
            stats = numeric_stats_pandas(series)
            present_values = series.loc[series.notnull()].astype(
                str(series.dtype).lower()
            )
            stats["n_zeros"] = series_description["count"] - np.count_nonzero(
                present_values
            )
            stats["histogram_data"] = present_values
            finite_values = present_values
        else:
            values = series.values
            present_values = values[~np.isnan(values)]
            finite_values = values[np.isfinite(values)]
            stats = numeric_stats_numpy(present_values)
            stats["histogram_data"] = finite_values

        stats.update(
            {
                "mad": mad(present_values),
                "scatter_data": series,  # For complex
                "p_infinite": n_infinite / series_description["n"],
                "n_infinite": n_infinite,
            }
        )

        chi_squared_threshold = config["vars"]["num"]["chi_squared_threshold"].get(
            float
        )
        if chi_squared_threshold > 0.0:
            histogram, _ = np.histogram(finite_values, bins="auto")
            stats["chi_squared"] = chisquare(histogram)

        stats["range"] = stats["max"] - stats["min"]
        stats.update(
            {
                f"{percentile:.0%}": value
                for percentile, value in series.quantile(quantiles).to_dict().items()
            }
        )
        stats["iqr"] = stats["75%"] - stats["25%"]
        stats["cv"] = stats["std"] / stats["mean"] if stats["mean"] else np.NaN
        stats["p_zeros"] = stats["n_zeros"] / series_description["n"]

        stats["monotonic_increase"] = series.is_monotonic_increasing
        stats["monotonic_decrease"] = series.is_monotonic_decreasing

        stats["monotonic_increase_strict"] = (
            stats["monotonic_increase"] and series.is_unique
        )
        stats["monotonic_decrease_strict"] = (
            stats["monotonic_decrease"] and series.is_unique
        )

        stats.update(histogram_compute(finite_values, series_description["n_distinct"]))

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
            "min": pd.Timestamp.to_pydatetime(series.min()),
            "max": pd.Timestamp.to_pydatetime(series.max()),
        }

        stats["range"] = stats["max"] - stats["min"]

        values = series[series.notnull()].values.astype(np.int64) // 10 ** 9

        chi_squared_threshold = config["vars"]["num"]["chi_squared_threshold"].get(
            float
        )
        if chi_squared_threshold > 0.0:
            histogram, _ = np.histogram(values, bins="auto")
            stats["chi_squared"] = chisquare(histogram)

        stats.update(histogram_compute(values, series_description["n_distinct"]))
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

        stats.update(
            histogram_compute(
                value_counts, len(value_counts), name="histogram_frequencies"
            )
        )

        chi_squared_threshold = config["vars"]["num"]["chi_squared_threshold"].get(
            float
        )
        if chi_squared_threshold > 0.0:
            stats["chi_squared"] = list(chisquare(value_counts.values))

        check_length = config["vars"]["cat"]["length"].get(bool)
        if check_length:
            stats.update(length_summary(series))
            stats.update(
                histogram_compute(
                    stats["length"], stats["length"].nunique(), name="histogram_length"
                )
            )

        check_unicode = config["vars"]["cat"]["unicode"].get(bool)
        if check_unicode:
            stats.update(unicode_summary(series))

            stats["category_alias_counts"].index = stats[
                "category_alias_counts"
            ].index.str.replace("_", " ")

        coerce_str_to_date = config["vars"]["cat"]["coerce_str_to_date"].get(bool)
        if coerce_str_to_date:
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
        series = series.apply(urlsplit)

        stats = url_summary(series)

        # Only run if at least 1 non-missing value
        value_counts = series_description["value_counts_without_nan"]

        stats["top"] = value_counts.index[0]
        stats["freq"] = value_counts.iloc[0]

        return stats

    def describe_file_1d(series: pd.Series, series_description: dict) -> dict:
        if "p_series" not in series_description:
            series = series[~series.isnull()].astype(str)
            series = series.map(Path)
            series_description["p_series"] = series
        else:
            series = series_description["p_series"]

        stats = file_summary(series)

        series_description.update(describe_path_1d(series, series_description))
        stats.update(
            histogram_compute(
                stats["file_size"],
                stats["file_size"].nunique(),
                name="histogram_file_size",
            )
        )

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
        if "p_series" not in series_description:
            series = series[~series.isnull()].astype(str)
            series = series.map(Path)
        else:
            series = series_description["p_series"]
            del series_description["p_series"]

        stats = path_summary(series)

        # Only run if at least 1 non-missing value
        value_counts = series_description["value_counts_without_nan"]

        stats["top"] = value_counts.index[0]
        stats["freq"] = value_counts.iloc[0]

        return stats

    def describe_image_1d(series: pd.Series, series_description: dict):
        if "p_series" not in series_description:
            series = series[~series.isnull()].astype(str)
            series = series.map(Path)
            series_description["p_series"] = series
        else:
            series = series_description["p_series"]

        extract_exif = config["vars"]["image"]["exif"].get(bool)

        stats = image_summary(series, extract_exif)

        series_description.update(describe_file_1d(series, series_description))

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

    # Make sure pd.NA is not in the series
    series = series.fillna(np.nan)

    # Infer variable types
    # TODO: use visions for type inference
    # https://github.com/dylan-profiler/visions
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
            Variable.TYPE_IMAGE: describe_image_1d,
            Variable.TYPE_FILE: describe_file_1d,
        }

        if series_description["type"] in type_to_func:
            series_description.update(
                type_to_func[series_description["type"]](series, series_description)
            )
        else:
            raise ValueError("Unexpected type")

    # light weight of series_description
    if "value_counts_with_nan" in series_description.keys():
        del series_description["value_counts_with_nan"]
    if "value_counts_without_nan" in series_description.keys():
        del series_description["value_counts_without_nan"]

    # Return the description obtained
    return series_description


def get_series_description(series):
    return describe_1d(series)


def get_series_descriptions(df, pbar):
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

    # Multiprocessing of Describe 1D for each column
    pool_size = config["pool_size"].get(int)
    if pool_size <= 0:
        pool_size = multiprocessing.cpu_count()

    args = [(column, series) for column, series in df.iteritems()]
    series_description = {}

    if pool_size == 1:
        for arg in args:
            pbar.set_postfix_str(f"Describe variable:{arg[0]}")
            column, description = multiprocess_1d(arg)
            series_description[column] = description
            pbar.update()
    else:
        # Store the original order
        original_order = {k: v for v, k in enumerate([column for column, _ in args])}

        # TODO: use `Pool` for Linux-based systems
        with multiprocessing.pool.ThreadPool(pool_size) as executor:
            for i, (column, description) in enumerate(
                executor.imap_unordered(multiprocess_1d, args)
            ):
                pbar.set_postfix_str(f"Describe variable:{column}")
                series_description[column] = description
                pbar.update()

        # Restore the original order
        series_description = dict(
            sorted(
                series_description.items(),
                key=lambda index: original_order.get(index[0]),
            )
        )

    # Mapping from column name to variable type
    sort = config["sort"].get(str)
    series_description = sort_column_names(series_description, sort)
    return series_description


def get_table_stats(df: pd.DataFrame, variable_stats: pd.DataFrame) -> dict:
    """General statistics for the DataFrame.

    Args:
      df: The DataFrame to describe.
      variable_stats: Previously calculated statistic on the DataFrame.

    Returns:
        A dictionary that contains the table statistics.
    """
    n = len(df)

    memory_size = df.memory_usage(deep=config["memory_deep"].get(bool)).sum()
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


def get_duplicates(df: pd.DataFrame, supported_columns) -> Optional[pd.DataFrame]:
    """Obtain the most occurring duplicate rows in the DataFrame.

    Args:
        df: the Pandas DataFrame.
        supported_columns: the columns to consider

    Returns:
        A subset of the DataFrame, ordered by occurrence.
    """
    n_head = config["duplicates"]["head"].get(int)

    if n_head > 0 and supported_columns:
        return (
            df[df.duplicated(subset=supported_columns, keep=False)]
            .groupby(supported_columns)
            .size()
            .reset_index(name="count")
            .nlargest(n_head, "count")
        )
    return None


def get_missing_diagrams(df: pd.DataFrame, table_stats: dict) -> dict:
    """Gets the rendered diagrams for missing values.

    Args:
        table_stats: The overall statistics for the DataFrame.
        df: The DataFrame on which to calculate the missing values.

    Returns:
        A dictionary containing the base64 encoded plots for each diagram that is active in the config (matrix, bar, heatmap, dendrogram).
    """

    def warn_missing(missing_name, error):
        warnings.warn(
            f"""There was an attempt to generate the {missing_name} missing values diagrams, but this failed.
    To hide this warning, disable the calculation
    (using `df.profile_report(missing_diagrams={{"{missing_name}": False}}`)
    If this is problematic for your use case, please report this as an issue:
    https://github.com/pandas-profiling/pandas-profiling/issues
    (include the error message: '{error}')"""
        )

    def missing_diagram(name) -> Callable:
        return {
            "bar": missing_bar,
            "bar2": missing_bar2,
            "matrix": missing_matrix,
            "heatmap": missing_heatmap,
            "dendrogram": missing_dendrogram,
        }[name]

    missing_map = {
        "bar": {"min_missing": 0, "name": "Count"},
        "bar2": {"min_missing": 0, "name": "Missing"},
        "matrix": {"min_missing": 0, "name": "Matrix"},
        "heatmap": {"min_missing": 2, "name": "Heatmap"},
        "dendrogram": {"min_missing": 1, "name": "Dendrogram"},
    }

    missing_map = {
        name: settings
        for name, settings in missing_map.items()
        if config["missing_diagrams"][name].get(bool)
        and table_stats["n_vars_with_missing"] >= settings["min_missing"]
    }
    missing = {}

    if len(missing_map) > 0:
        for name, settings in missing_map.items():
            try:
                if name != "heatmap" or (
                    table_stats["n_vars_with_missing"]
                    - table_stats["n_vars_all_missing"]
                    >= settings["min_missing"]
                ):
                    missing[name] = {
                        "name": settings["name"],
                        "matrix": missing_diagram(name)(df),
                    }
            except ValueError as e:
                warn_missing(name, e)

    return missing


def get_scatter_matrix(df, variables):
    if config["interactions"]["continuous"].get(bool):
        continuous_variables = [
            column for column, type in variables.items() if type == Variable.TYPE_NUM
        ]

        targets = config["interactions"]["targets"].get(list)
        if len(targets) == 0:
            targets = continuous_variables

        scatter_matrix = {x: {y: "" for y in continuous_variables} for x in targets}

        for x in targets:
            for y in continuous_variables:
                if x in continuous_variables:
                    # check if any na still exists, and remove it before computing scatter matrix
                    df_temp = df[[x,y]].dropna()
                    scatter_matrix[x][y] = scatter_pairwise(df_temp[x], df_temp[y], x, y)
    else:
        scatter_matrix = {}

    return scatter_matrix


def get_messages(table_stats, series_description, correlations):
    messages = check_table_messages(table_stats)
    for col, description in series_description.items():
        messages += check_variable_messages(col, description)
    messages += check_correlation_messages(correlations)
    messages.sort(key=lambda message: str(message.message_type))
    return messages
