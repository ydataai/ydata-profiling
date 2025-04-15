# mypy: ignore-errors

"""Correlations between variables."""

import warnings
from typing import Dict, List, Optional, Sized, no_type_check

import numpy as np
import pandas as pd

from ydata_profiling.config import Settings

try:
    from pandas.core.base import DataError
except ImportError:
    from pandas.errors import DataError


class CorrelationBackend:
    """Helper class to select and cache the appropriate correlation backend (Pandas or Spark)."""

    @no_type_check
    def __init__(self, df: Sized):
        """Determine backend once and store it for all correlation computations."""
        if isinstance(df, pd.DataFrame):
            from ydata_profiling.model.pandas import (
                correlations_pandas as correlation_backend,  # type: ignore
            )
        else:
            from ydata_profiling.model.spark import (
                correlations_spark as correlation_backend,  # type: ignore
            )

        self.backend = correlation_backend

    def get_method(self, method_name: str):  # noqa: ANN201
        """Retrieve the appropriate correlation method class from the backend."""
        if hasattr(self.backend, method_name):
            return getattr(self.backend, method_name)
        raise AttributeError(
            f"Correlation method '{method_name}' is not available in the backend."
        )


class Correlation:
    _method_name: str = ""

    def compute(
        self, config: Settings, df: Sized, summary: dict, backend: CorrelationBackend
    ) -> Optional[Sized]:
        """Computes correlation using the correct backend (Pandas or Spark)."""
        try:
            method = backend.get_method(self._method_name)
        except AttributeError as ex:
            raise NotImplementedError() from ex
        else:
            return method(config, df, summary)


class Auto(Correlation):
    """Automatically selects the appropriate correlation method based on the DataFrame type."""

    _method_name = "auto_compute"


class Spearman(Correlation):
    _method_name = "spearman_compute"


class Pearson(Correlation):
    _method_name = "pearson_compute"


class Kendall(Correlation):
    _method_name = "kendall_compute"


class Cramers(Correlation):
    _method_name = "cramers_compute"


class PhiK(Correlation):
    _method_name = "phik_compute"


def warn_correlation(correlation_name: str, error: str) -> None:
    warnings.warn(
        f"""There was an attempt to calculate the {correlation_name} correlation, but this failed.
To hide this warning, disable the calculation
(using `df.profile_report(correlations={{\"{correlation_name}\": {{\"calculate\": False}}}})`
If this is problematic for your use case, please report this as an issue:
https://github.com/ydataai/ydata-profiling/issues
(include the error message: '{error}')"""
    )


def calculate_correlation(
    config: Settings, df: Sized, correlation_name: str, summary: dict
) -> Optional[Sized]:
    """Calculate the correlation coefficients between variables for the correlation types selected in the config
    (auto, pearson, spearman, kendall, phi_k, cramers).

    Args:
        config: report Settings object
        df: The DataFrame with variables.
        correlation_name:
        summary: summary dictionary

    Returns:
        The correlation matrices for the given correlation measures. Return None if correlation is empty.
    """
    backend = CorrelationBackend(df)

    correlation_measures = {
        "auto": Auto,
        "pearson": Pearson,
        "spearman": Spearman,
        "kendall": Kendall,
        "cramers": Cramers,
        "phi_k": PhiK,
    }

    correlation = None
    try:
        correlation = correlation_measures[correlation_name]().compute(
            config, df, summary, backend
        )
    except (ValueError, AssertionError, TypeError, DataError, IndexError) as e:
        warn_correlation(correlation_name, str(e))

    return correlation if correlation is not None and len(correlation) > 0 else None


def perform_check_correlation(
    correlation_matrix: pd.DataFrame, threshold: float
) -> Dict[str, List[str]]:
    """Check whether selected variables are highly correlated values in the correlation matrix.

    Args:
        correlation_matrix: The correlation matrix for the DataFrame.
        threshold:.

    Returns:
        The variables that are highly correlated.
    """

    cols = correlation_matrix.columns
    bool_index = abs(correlation_matrix.values) >= threshold
    np.fill_diagonal(bool_index, False)
    return {
        col: cols[bool_index[i]].values.tolist()
        for i, col in enumerate(cols)
        if any(bool_index[i])
    }


def get_active_correlations(config: Settings) -> List[str]:
    correlation_names = [
        correlation_name
        for correlation_name in config.correlations.keys()
        if config.correlations[correlation_name].calculate
    ]
    return correlation_names
