import warnings
from typing import Any, Callable, Dict, Optional

import pandas as pd
from multimethod import multimethod

from pandas_profiling.config import Settings


@multimethod
def missing_bar(config: Settings, df: Any) -> str:
    raise NotImplementedError()


@multimethod
def missing_matrix(config: Settings, df: Any) -> str:
    raise NotImplementedError()


@multimethod
def missing_heatmap(config: Settings, df: Any) -> str:
    raise NotImplementedError()


@multimethod
def missing_dendrogram(config: Settings, df: Any) -> str:
    raise NotImplementedError()


def get_missing_active(config: Settings, table_stats: dict) -> Dict[Any, Any]:
    """

    Args:
        config: report Settings object
        table_stats: The overall statistics for the DataFrame.

    Returns:

    """
    missing_map = {
        "bar": {
            "min_missing": 0,
            "name": "Count",
            "caption": "A simple visualization of nullity by column.",
            "function": missing_bar,
        },
        "matrix": {
            "min_missing": 0,
            "name": "Matrix",
            "caption": "Nullity matrix is a data-dense display which lets you quickly visually pick out patterns in data completion.",
            "function": missing_matrix,
        },
        "heatmap": {
            "min_missing": 2,
            "name": "Heatmap",
            "caption": "The correlation heatmap measures nullity correlation: how strongly the presence or absence of one variable affects the presence of another.",
            "function": missing_heatmap,
        },
        "dendrogram": {
            "min_missing": 1,
            "name": "Dendrogram",
            "caption": "The dendrogram allows you to more fully correlate variable completion, revealing trends deeper than the pairwise ones visible in the correlation heatmap.",
            "function": missing_dendrogram,
        },
    }

    missing_map = {
        name: settings
        for name, settings in missing_map.items()
        if (
            config.missing_diagrams[name]
            and table_stats["n_vars_with_missing"] >= settings["min_missing"]
        )
        and (
            name != "heatmap"
            or (
                table_stats["n_vars_with_missing"] - table_stats["n_vars_all_missing"]
                >= settings["min_missing"]
            )
        )
    }

    return missing_map


def handle_missing(name: str, fn: Callable) -> Callable:
    def inner(*args, **kwargs) -> Any:
        def warn_missing(missing_name: str, error: str) -> None:
            warnings.warn(
                f"""There was an attempt to generate the {missing_name} missing values diagrams, but this failed.
To hide this warning, disable the calculation
(using `df.profile_report(missing_diagrams={{"{missing_name}": False}}`)
If this is problematic for your use case, please report this as an issue:
https://github.com/pandas-profiling/pandas-profiling/issues
(include the error message: '{error}')"""
            )

        try:
            return fn(*args, *kwargs)
        except ValueError as e:
            warn_missing(name, str(e))

    return inner


def get_missing_diagram(
    config: Settings, df: pd.DataFrame, settings: Dict[str, Any]
) -> Optional[Dict[str, Any]]:
    """Gets the rendered diagrams for missing values.

    Args:
        config: report Settings object
        df: The DataFrame on which to calculate the missing values.
        settings: missing diagram name, caption and function

    Returns:
        A dictionary containing the base64 encoded plots for each diagram that is active in the config (matrix, bar, heatmap, dendrogram).
    """

    if len(df) == 0:
        return None

    result = handle_missing(settings["name"], settings["function"])(config, df)
    if result is None:
        return None

    missing = {
        "name": settings["name"],
        "caption": settings["caption"],
        "matrix": result,
    }

    return missing
