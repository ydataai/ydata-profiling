import importlib
import warnings
from typing import Any, Callable, Dict, Optional, Sized

import pandas as pd

from ydata_profiling.config import Settings
from ydata_profiling.i18n import _


class MissingDataBackend:
    """Helper class to select and cache the appropriate missing-data backend (Pandas or Spark)."""

    def __init__(self, df: Sized):
        """Determine backend once and store it for all missing-data computations."""
        if isinstance(df, pd.DataFrame):
            self.backend_module = "ydata_profiling.model.pandas.missing_pandas"
        else:
            self.backend_module = "ydata_profiling.model.spark.missing_spark"

        self.module = importlib.import_module(self.backend_module)

    def get_method(self, method_name: str) -> Callable:
        """Retrieve the appropriate missing-data function from the backend module."""
        try:
            return getattr(self.module, method_name)
        except AttributeError as ex:
            raise AttributeError(
                f"Missing-data function '{method_name}' is not available in {self.backend_module}."
            ) from ex


class MissingData:
    _method_name: str = ""

    def compute(
        self, config: Settings, df: Sized, backend: MissingDataBackend
    ) -> Optional[Sized]:
        """Computes correlation using the correct backend (Pandas or Spark)."""
        try:
            method = backend.get_method(self._method_name)
        except AttributeError as ex:
            raise NotImplementedError() from ex
        else:
            return method(config, df)


class MissingBar(MissingData):
    _method_name = "missing_bar"


class MissingMatrix(MissingData):
    _method_name = "missing_matrix"


class MissingHeatmap(MissingData):
    _method_name = "missing_heatmap"


def get_missing_active(config: Settings, table_stats: dict) -> Dict[str, Any]:
    """

    Args:
        config: report Settings object
        table_stats: The overall statistics for the DataFrame.

    Returns:

    """

    missing_map = {
        "bar": {
            "min_missing": 0,
            "name": _("core.model.bar_count"),
            "caption": _("core.model.bar_caption"),
            "function": MissingBar(),
        },
        "matrix": {
            "min_missing": 0,
            "name": _("core.model.matrix"),
            "caption":  _("core.model.matrix_caption"),
            "function": MissingMatrix(),
        },
        "heatmap": {
            "min_missing": 2,
            "name": _("core.model.heatmap"),
            "caption": _("core.model.heatmap_caption"),
            "function": MissingHeatmap(),
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


def get_missing_diagram(
    config: Settings, df: pd.DataFrame, settings: Dict[str, Any]
) -> Optional[Dict[str, Any]]:
    """Gets the rendered diagrams for missing values.

    Args:
        config: report Settings object
        df: The DataFrame on which to calculate the missing values.
        settings: missing diagram name, caption and function

    Returns:
        A dictionary containing the base64 encoded plots for each diagram that is active in the config (matrix, bar, heatmap).
    """
    backend = MissingDataBackend(df)

    missing_func = settings.get("function")
    if missing_func is None:
        return None  # No function defined, skip execution

    try:
        result = missing_func.compute(config, df, backend)
    except ValueError as e:
        warnings.warn(
            f"""There was an attempt to generate the {settings['name']} missing values diagrams, but this failed.
        To hide this warning, disable the calculation
        (using `df.profile_report(missing_diagrams={{"{settings['name']}": False}}`)
        If this is problematic for your use case, please report this as an issue:
        https://github.com/ydataai/ydata-profiling/issues
        (include the error message: '{e}')"""
        )
        return None
    else:
        return {
            "name": settings["name"],
            "caption": settings["caption"],
            "matrix": result,
        }
