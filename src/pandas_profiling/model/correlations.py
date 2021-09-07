"""Correlations between variables."""
import warnings
from typing import Any, Callable, Dict, List, Optional, Sized

import numpy as np
import pandas as pd
from multimethod import multimethod
from pandas.core.base import DataError

from pandas_profiling.config import Settings
from pandas_profiling.utils.str import camel_to_snake


class RegistryBase(type):
    REGISTRY: Dict[str, Callable] = {}

    @classmethod
    def get_registry(mcs) -> dict:
        return dict(mcs.REGISTRY)

    @classmethod
    def register(mcs, cls) -> None:
        mcs.REGISTRY[cls.__name__] = cls


class Correlation:
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        RegistryBase.register(cls)

    @staticmethod
    def compute(config: Settings, df: Sized, summary: dict) -> Optional[Sized]:
        raise NotImplementedError()


class Spearman(Correlation):
    @staticmethod
    @multimethod
    def compute(config: Settings, df: Sized, summary: dict) -> Optional[Sized]:
        raise NotImplementedError()


class Pearson(Correlation):
    @staticmethod
    @multimethod
    def compute(config: Settings, df: Sized, summary: dict) -> Optional[Sized]:
        raise NotImplementedError()


class Kendall(Correlation):
    @staticmethod
    @multimethod
    def compute(config: Settings, df: Sized, summary: dict) -> Optional[Sized]:
        raise NotImplementedError()


class Cramers(Correlation):
    @staticmethod
    @multimethod
    def compute(config: Settings, df: Sized, summary: dict) -> Optional[Sized]:
        raise NotImplementedError()


class PhiK(Correlation):
    @staticmethod
    @multimethod
    def compute(config: Settings, df: Sized, summary: dict) -> Optional[Sized]:
        raise NotImplementedError()


def warn_correlation(correlation_name: str, error: str) -> None:
    warnings.warn(
        f"""There was an attempt to calculate the {correlation_name} correlation, but this failed.
To hide this warning, disable the calculation
(using `df.profile_report(correlations={{\"{correlation_name}\": {{\"calculate\": False}}}})`
If this is problematic for your use case, please report this as an issue:
https://github.com/pandas-profiling/pandas-profiling/issues
(include the error message: '{error}')"""
    )


def get_correlations() -> dict:
    correlation_measures = {
        camel_to_snake(k): v for k, v in RegistryBase.get_registry().items()
    }
    return correlation_measures


def get_active_correlations(config: Settings) -> Dict[str, Any]:
    correlation_names = {
        name: value
        for name, value in get_correlations().items()
        if config.correlations[name].calculate
    }
    return correlation_names


def calculate_correlation(
    config: Settings, df: Sized, correlation_name: str, summary: dict
) -> Optional[Sized]:
    """Calculate the correlation coefficients between variables for the correlation types selected in the config
    (pearson, spearman, kendall, phi_k, cramers, & custom).

    Args:
        config: report Settings object
        df: The DataFrame with variables.
        correlation_name:
        summary: summary dictionary

    Returns:
        The correlation matrices for the given correlation measures. Return None if correlation is empty.
    """

    correlation_measures = get_active_correlations(config)

    correlation = None
    try:
        correlation = correlation_measures[correlation_name].compute(
            config, df, summary
        )
    except (ValueError, AssertionError, TypeError, DataError, IndexError) as e:
        warn_correlation(correlation_name, str(e))

    if correlation is not None and len(correlation) <= 0:
        correlation = None

    return correlation


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
