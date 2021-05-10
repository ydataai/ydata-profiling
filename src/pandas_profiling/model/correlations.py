"""Correlations between variables."""
import itertools
import warnings
from typing import Dict, List, Optional

import numpy as np
import pandas as pd
from pandas.core.base import DataError
from scipy import stats

from pandas_profiling.config import Settings


class Correlation:
    @staticmethod
    def compute(
        config: Settings, df: pd.DataFrame, summary: dict
    ) -> Optional[pd.DataFrame]:
        raise NotImplementedError()


class Spearman(Correlation):
    @staticmethod
    def compute(
        config: Settings, df: pd.DataFrame, summary: dict
    ) -> Optional[pd.DataFrame]:
        return df.corr(method="spearman")


class Pearson(Correlation):
    @staticmethod
    def compute(
        config: Settings, df: pd.DataFrame, summary: dict
    ) -> Optional[pd.DataFrame]:
        return df.corr(method="pearson")


class Kendall(Correlation):
    @staticmethod
    def compute(
        config: Settings, df: pd.DataFrame, summary: dict
    ) -> Optional[pd.DataFrame]:
        return df.corr(method="kendall")


class Cramers(Correlation):
    @staticmethod
    def _cramers_corrected_stat(
        confusion_matrix: pd.DataFrame, correction: bool
    ) -> float:
        """Calculate the Cramer's V corrected stat for two variables.

        Args:
            confusion_matrix: Crosstab between two variables.
            correction: Should the correction be applied?

        Returns:
            The Cramer's V corrected stat for the two variables.
        """
        chi2 = stats.chi2_contingency(confusion_matrix, correction=correction)[0]
        n = confusion_matrix.sum().sum()
        phi2 = chi2 / n
        r = confusion_matrix.shape[0]
        k = confusion_matrix.shape[1] if len(confusion_matrix.shape) > 1 else 1

        # Deal with NaNs later on
        with np.errstate(divide="ignore", invalid="ignore"):
            phi2corr = max(0.0, phi2 - ((k - 1.0) * (r - 1.0)) / (n - 1.0))
            rcorr = r - ((r - 1.0) ** 2.0) / (n - 1.0)
            kcorr = k - ((k - 1.0) ** 2.0) / (n - 1.0)
            rkcorr = min((kcorr - 1.0), (rcorr - 1.0))
            if rkcorr == 0.0:
                corr = 1.0
            else:
                corr = np.sqrt(phi2corr / rkcorr)
        return corr

    @staticmethod
    def compute(
        config: Settings, df: pd.DataFrame, summary: dict
    ) -> Optional[pd.DataFrame]:
        threshold = config.categorical_maximum_correlation_distinct

        categoricals = {
            key
            for key, value in summary.items()
            if value["type"] in {"Categorical", "Boolean"}
            and value["n_distinct"] <= threshold
        }

        if len(categoricals) <= 1:
            return None

        matrix = np.zeros((len(categoricals), len(categoricals)))
        np.fill_diagonal(matrix, 1.0)
        correlation_matrix = pd.DataFrame(
            matrix,
            index=categoricals,
            columns=categoricals,
        )

        for name1, name2 in itertools.combinations(categoricals, 2):
            confusion_matrix = pd.crosstab(df[name1], df[name2])
            correlation_matrix.loc[name2, name1] = Cramers._cramers_corrected_stat(
                confusion_matrix, correction=True
            )
            correlation_matrix.loc[name1, name2] = correlation_matrix.loc[name2, name1]
        return correlation_matrix


class PhiK(Correlation):
    @staticmethod
    def compute(
        config: Settings, df: pd.DataFrame, summary: dict
    ) -> Optional[pd.DataFrame]:
        threshold = config.categorical_maximum_correlation_distinct
        intcols = {
            key
            for key, value in summary.items()
            # DateTime currently excluded
            # In some use cases, it makes sense to convert it to interval
            # See https://github.com/KaveIO/PhiK/issues/7
            if value["type"] == "Numeric" and 1 < value["n_distinct"]
        }

        selcols = {
            key
            for key, value in summary.items()
            if value["type"] != "Unsupported" and 1 < value["n_distinct"] <= threshold
        }
        selcols = selcols.union(intcols)

        if len(selcols) <= 1:
            return None

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            from phik import phik_matrix

            correlation = phik_matrix(df[selcols], interval_cols=list(intcols))

        return correlation


def warn_correlation(correlation_name: str, error: str) -> None:
    warnings.warn(
        f"""There was an attempt to calculate the {correlation_name} correlation, but this failed.
To hide this warning, disable the calculation
(using `df.profile_report(correlations={{\"{correlation_name}\": {{\"calculate\": False}}}})`
If this is problematic for your use case, please report this as an issue:
https://github.com/pandas-profiling/pandas-profiling/issues
(include the error message: '{error}')"""
    )


def calculate_correlation(
    config: Settings, df: pd.DataFrame, correlation_name: str, summary: dict
) -> Optional[pd.DataFrame]:
    """Calculate the correlation coefficients between variables for the correlation types selected in the config
    (pearson, spearman, kendall, phi_k, cramers).

    Args:
        df: The DataFrame with variables.
        correlation_name:
        summary: summary dictionary

    Returns:
        The correlation matrices for the given correlation measures. Return None if correlation is empty.
    """

    if len(df) == 0:
        return None

    correlation_measures = {
        "pearson": Pearson,
        "spearman": Spearman,
        "kendall": Kendall,
        "cramers": Cramers,
        "phi_k": PhiK,
    }

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
