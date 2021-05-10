"""Compute statistical description of datasets."""

import multiprocessing
import multiprocessing.pool
import warnings
from collections import Counter
from typing import Callable, List, Optional, Tuple

import numpy as np
import pandas as pd
from tqdm import tqdm
from visions import VisionsTypeset

from pandas_profiling.config import Settings
from pandas_profiling.model.messages import (
    Message,
    check_correlation_messages,
    check_table_messages,
    check_variable_messages,
)
from pandas_profiling.model.summarizer import BaseSummarizer
from pandas_profiling.visualisation.missing import (
    missing_bar,
    missing_dendrogram,
    missing_heatmap,
    missing_matrix,
)
from pandas_profiling.visualisation.plot import scatter_pairwise


def describe_1d(
    config: Settings,
    series: pd.Series,
    summarizer: BaseSummarizer,
    typeset: VisionsTypeset,
) -> dict:
    """Describe a series (infer the variable type, then calculate type-specific values).

    Args:
        config: report Settings object
        series: The Series to describe.
        summarizer: Summarizer object
        typeset: Typeset

    Returns:
        A Series containing calculated series description values.
    """

    # Make sure pd.NA is not in the series
    series = series.fillna(np.nan)

    # get `infer_dtypes` (bool) from config
    if config.infer_dtypes:
        # Infer variable types
        vtype = typeset.infer_type(series)
        series = typeset.cast_to_inferred(series)
    else:
        # Detect variable types from pandas dataframe (df.dtypes).
        # [new dtypes, changed using `astype` function are now considered]
        vtype = typeset.detect_type(series)

    return summarizer.summarize(config, series, dtype=vtype)


def sort_column_names(dct: dict, sort: Optional[str]) -> dict:
    if sort is None:
        return dct

    sort = sort.lower()
    if sort.startswith("asc"):
        dct = dict(sorted(dct.items(), key=lambda x: x[0].casefold()))
    elif sort.startswith("desc"):
        dct = dict(sorted(dct.items(), key=lambda x: x[0].casefold(), reverse=True))
    else:
        raise ValueError('"sort" should be "ascending", "descending" or None.')
    return dct


def get_series_descriptions(
    config: Settings,
    df: pd.DataFrame,
    summarizer: BaseSummarizer,
    typeset: VisionsTypeset,
    pbar: tqdm,
) -> dict:
    def multiprocess_1d(args: tuple) -> Tuple[str, dict]:
        """Wrapper to process series in parallel.

        Args:
            column: The name of the column.
            series: The series values.

        Returns:
            A tuple with column and the series description.
        """
        column, series = args
        return column, describe_1d(config, series, summarizer, typeset)

    pool_size = config.pool_size

    # Multiprocessing of Describe 1D for each column
    if pool_size <= 0:
        pool_size = multiprocessing.cpu_count()

    args = [(name, series) for name, series in df.iteritems()]
    series_description = {}

    if pool_size == 1:
        for arg in args:
            pbar.set_postfix_str(f"Describe variable:{arg[0]}")
            column, description = multiprocess_1d(arg)
            series_description[column] = description
            pbar.update()
    else:
        # TODO: use `Pool` for Linux-based systems
        with multiprocessing.pool.ThreadPool(pool_size) as executor:
            for i, (column, description) in enumerate(
                executor.imap_unordered(multiprocess_1d, args)
            ):
                pbar.set_postfix_str(f"Describe variable:{column}")
                series_description[column] = description
                pbar.update()

        # Restore the original order
        series_description = {k: series_description[k] for k in df.columns}

    # Mapping from column name to variable type
    series_description = sort_column_names(series_description, config.sort)
    return series_description


def get_table_stats(config: Settings, df: pd.DataFrame, variable_stats: dict) -> dict:
    """General statistics for the DataFrame.

    Args:
        config: report Settings object
        df: The DataFrame to describe.
        variable_stats: Previously calculated statistic on the DataFrame.

    Returns:
        A dictionary that contains the table statistics.
    """
    n = len(df)

    memory_size = df.memory_usage(deep=config.memory_deep).sum()
    record_size = float(memory_size) / n if n > 0 else 0

    table_stats = {
        "n": n,
        "n_var": len(df.columns),
        "memory_size": memory_size,
        "record_size": record_size,
        "n_cells_missing": 0,
        "n_vars_with_missing": 0,
        "n_vars_all_missing": 0,
    }

    for series_summary in variable_stats.values():
        if "n_missing" in series_summary and series_summary["n_missing"] > 0:
            table_stats["n_vars_with_missing"] += 1
            table_stats["n_cells_missing"] += series_summary["n_missing"]
            if series_summary["n_missing"] == n:
                table_stats["n_vars_all_missing"] += 1

    table_stats["p_cells_missing"] = (
        table_stats["n_cells_missing"] / (table_stats["n"] * table_stats["n_var"])
        if table_stats["n"] > 0
        else 0
    )

    # Variable type counts
    table_stats.update(
        {"types": dict(Counter([v["type"] for v in variable_stats.values()]))}
    )

    return table_stats


def get_missing_diagrams(config: Settings, df: pd.DataFrame, table_stats: dict) -> dict:
    """Gets the rendered diagrams for missing values.

    Args:
        table_stats: The overall statistics for the DataFrame.
        df: The DataFrame on which to calculate the missing values.

    Returns:
        A dictionary containing the base64 encoded plots for each diagram that is active in the config (matrix, bar, heatmap, dendrogram).
    """

    if len(df) == 0:
        return {}

    def warn_missing(missing_name: str, error: str) -> None:
        warnings.warn(
            f"""There was an attempt to generate the {missing_name} missing values diagrams, but this failed.
    To hide this warning, disable the calculation
    (using `df.profile_report(missing_diagrams={{"{missing_name}": False}}`)
    If this is problematic for your use case, please report this as an issue:
    https://github.com/pandas-profiling/pandas-profiling/issues
    (include the error message: '{error}')"""
        )

    def missing_diagram(name: str) -> Callable:
        return {
            "bar": missing_bar,
            "matrix": missing_matrix,
            "heatmap": missing_heatmap,
            "dendrogram": missing_dendrogram,
        }[name]

    missing_map = {
        "bar": {
            "min_missing": 0,
            "name": "Count",
            "caption": "A simple visualization of nullity by column.",
        },
        "matrix": {
            "min_missing": 0,
            "name": "Matrix",
            "caption": "Nullity matrix is a data-dense display which lets you quickly visually pick out patterns in data completion.",
        },
        "heatmap": {
            "min_missing": 2,
            "name": "Heatmap",
            "caption": "The correlation heatmap measures nullity correlation: how strongly the presence or absence of one variable affects the presence of another.",
        },
        "dendrogram": {
            "min_missing": 1,
            "name": "Dendrogram",
            "caption": "The dendrogram allows you to more fully correlate variable completion, revealing trends deeper than the pairwise ones visible in the correlation heatmap.",
        },
    }

    missing_map = {
        name: settings
        for name, settings in missing_map.items()
        if config.missing_diagrams[name]
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
                        "caption": settings["caption"],
                        "matrix": missing_diagram(name)(config, df),
                    }
            except ValueError as e:
                warn_missing(name, str(e))

    return missing


def get_scatter_matrix(
    config: Settings, df: pd.DataFrame, continuous_variables: list
) -> dict:
    if not config.interactions.continuous:
        return {}

    targets = config.interactions.targets
    if len(targets) == 0:
        targets = continuous_variables

    scatter_matrix = {x: {y: "" for y in continuous_variables} for x in targets}

    for x in targets:
        for y in continuous_variables:
            if x in continuous_variables:
                if y == x:
                    df_temp = df[[x]].dropna()
                else:
                    df_temp = df[[x, y]].dropna()
                scatter_matrix[x][y] = scatter_pairwise(
                    config, df_temp[x], df_temp[y], x, y
                )

    return scatter_matrix


def get_messages(
    config: Settings, table_stats: dict, series_description: dict, correlations: dict
) -> List[Message]:
    messages = check_table_messages(table_stats)
    for col, description in series_description.items():
        messages += check_variable_messages(config, col, description)
    messages += check_correlation_messages(config, correlations)
    messages.sort(key=lambda message: str(message.message_type))
    return messages
