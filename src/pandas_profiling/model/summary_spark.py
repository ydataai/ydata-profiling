"""Compute statistical description of datasets."""

import warnings
from collections import Counter
from typing import Callable

from pandas_profiling.config import config as config
from pandas_profiling.model.dataframe_wrappers import (
    UNWRAPPED_DATAFRAME_WARNING,
    GenericDataFrame,
    SparkDataFrame,
    get_appropriate_wrapper,
)
from pandas_profiling.model.typeset import (
    SparkBoolean,
    SparkCategorical,
    SparkNumeric,
    SparkUnsupported,
)
from pandas_profiling.utils.dataframe import sort_column_names
from pandas_profiling.visualisation.missing import missing_bar
from pandas_profiling.visualisation.plot import spark_scatter_pairwise


def get_series_descriptions_spark(df: SparkDataFrame, summarizer, typeset, pbar):
    # check for unwrapped dataframes and warn
    if not isinstance(df, GenericDataFrame):
        warnings.warn(UNWRAPPED_DATAFRAME_WARNING)
        df_wrapper = get_appropriate_wrapper(df)
        df = df_wrapper(df)

    sort = config["sort"].get(str)

    schema_column_pairs = [
        {"name": i[0], "type": str(i[1].dataType)} for i in zip(df.columns, df.schema)
    ]

    numeric_cols = {
        pair["name"]
        for pair in filter(
            lambda pair: pair["type"] in SparkNumeric, schema_column_pairs
        )
    }
    categorical_cols = {
        pair["name"]
        for pair in filter(
            lambda pair: pair["type"] in SparkCategorical, schema_column_pairs
        )
    }
    boolean_cols = {
        pair["name"]
        for pair in filter(
            lambda pair: pair["type"] in SparkBoolean, schema_column_pairs
        )
    }
    supported_cols = numeric_cols.union(categorical_cols).union(boolean_cols)
    unsupported_cols = set(df.columns)
    unsupported_cols.difference_update(supported_cols)

    pbar.set_postfix_str(f"Describe variable type: Numeric")
    series_description = summarizer.summarize(
        SparkDataFrame(df.get_spark_df().select(list(numeric_cols))),
        engine=df.engine,
        dtype=SparkNumeric,
    )
    pbar.update(n=len(numeric_cols))

    pbar.set_postfix_str(f"Describe variable type: Categorical")
    series_description.update(
        summarizer.summarize(
            SparkDataFrame(df.get_spark_df().select(list(categorical_cols))),
            engine=df.engine,
            dtype=SparkCategorical,
        )
    )
    pbar.update(n=len(categorical_cols))

    pbar.set_postfix_str(f"Describe variable type: Boolean")
    series_description.update(
        summarizer.summarize(
            SparkDataFrame(df.get_spark_df().select(list(boolean_cols))),
            engine=df.engine,
            dtype=SparkBoolean,
        )
    )
    pbar.update(n=len(boolean_cols))

    pbar.set_postfix_str(f"Describe variable type: Others")
    series_description.update(
        summarizer.summarize(
            SparkDataFrame(df.get_spark_df().select(list(unsupported_cols))),
            engine=df.engine,
            dtype=SparkUnsupported,
        )
    )
    pbar.update(n=len(unsupported_cols))

    # Restore the original order
    series_description = sort_column_names(series_description, sort)

    return series_description


def get_table_stats_spark(df: SparkDataFrame, variable_stats: dict) -> dict:
    n = len(df)

    memory_size = df.get_memory_usage(deep=config["memory_deep"].get(bool)).sum()
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

    table_stats["p_cells_missing"] = table_stats["n_cells_missing"] / (
        table_stats["n"] * table_stats["n_var"]
    )

    supported_columns = [
        k for k, v in variable_stats.items() if v["type"] != SparkUnsupported
    ]
    table_stats["n_duplicates"] = (
        df.get_duplicate_rows_count(subset=supported_columns)
        if len(supported_columns) > 0
        else 0
    )
    table_stats["p_duplicates"] = (
        (table_stats["n_duplicates"] / len(df))
        if (len(supported_columns) > 0 and len(df) > 0)
        else 0
    )

    # Variable type counts
    table_stats.update(
        {"types": dict(Counter([v["type"] for v in variable_stats.values()]))}
    )

    return table_stats


def get_missing_diagrams_spark(df: SparkDataFrame, table_stats: dict) -> dict:
    """
    awaiting missingno submission

    Args:
        df:
        table_stats:

    Returns:

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
        }[name]

    missing_map = {
        "bar": {
            "min_missing": 0,
            "name": "Count",
            "caption": "A simple visualization of nullity by column.",
        },
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
                        "caption": settings["caption"],
                        "matrix": missing_diagram(name)(df),
                    }
            except ValueError as e:
                warn_missing(name, e)

    return missing


def get_scatter_matrix_spark(df, continuous_variables):
    scatter_matrix = {}
    if config["interactions"]["continuous"].get(bool):
        targets = config["interactions"]["targets"].get(list)
        if len(targets) == 0:
            targets = continuous_variables

        scatter_matrix = {x: {y: "" for y in continuous_variables} for x in targets}

        df.persist()

        for x in targets:
            for y in continuous_variables:
                if x in continuous_variables:
                    scatter_matrix[x][y] = spark_scatter_pairwise(df, x, y)
    return scatter_matrix
