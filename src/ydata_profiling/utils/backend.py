"""
    File with backend utilities and helper functions to check the backend being used
"""
import importlib
from typing import Callable, Optional, Sized, Union

import pandas as pd


def is_pyspark_installed() -> bool:
    """Check if PySpark is installed without importing it."""
    return importlib.util.find_spec("pyspark") is not None


class BaseBackend:
    """Base helper class to select and cache the appropriate backend (Pandas or Spark)."""

    _pandas_module: Optional[str] = None
    _spark_module: Optional[str] = None

    def __init__(self, df: Union[pd.DataFrame, Sized]):
        """Determine backend once and store it for all computations."""
        if isinstance(df, pd.DataFrame):
            module_path = self._pandas_module
        else:
            module_path = self._spark_module

        if module_path is None:
            raise ValueError("Backend module path not configured")

        self.module = importlib.import_module(module_path)
        self.module_path = module_path

    def get_method(self, method_name: str) -> Callable:
        """Retrieve the appropriate function from the backend module."""
        try:
            return getattr(self.module, method_name)
        except AttributeError as ex:
            raise AttributeError(
                f"Function '{method_name}' is not available in {self.module_path}."
            ) from ex
