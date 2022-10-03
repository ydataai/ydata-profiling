"""Correlations between variables."""
import itertools
import warnings
from typing import Optional

import numpy as np
import pandas as pd
from scipy import stats

from pandas_profiling.config import Settings
from pandas_profiling.model.correlations import (
    Cramers,
    Kendall,
    Pearson,
    PhiK,
    Spearman,
)


@Spearman.compute.register(Settings, pd.DataFrame, dict)
def pandas_spearman_compute(
    config: Settings, df: pd.DataFrame, summary: dict
) -> Optional[pd.DataFrame]:
    return df.corr(method="spearman")


@Pearson.compute.register(Settings, pd.DataFrame, dict)
def pandas_pearson_compute(
    config: Settings, df: pd.DataFrame, summary: dict
) -> Optional[pd.DataFrame]:
    return df.corr(method="pearson")


@Kendall.compute.register(Settings, pd.DataFrame, dict)
def pandas_kendall_compute(
    config: Settings, df: pd.DataFrame, summary: dict
) -> Optional[pd.DataFrame]:
    return df.corr(method="kendall")


def _cramers_corrected_stat(confusion_matrix: pd.DataFrame, correction: bool) -> float:
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


@Cramers.compute.register(Settings, pd.DataFrame, dict)
def pandas_cramers_compute(
    config: Settings, df: pd.DataFrame, summary: dict
) -> Optional[pd.DataFrame]:
    threshold = config.categorical_maximum_correlation_distinct

    # `index` and `columns` must not be a set since Pandas 1.5,
    # so convert it to a list. The order of the list is arbitrary.
    categoricals = list(
        {
            key
            for key, value in summary.items()
            if value["type"] in {"Categorical", "Boolean"}
            and value["n_distinct"] <= threshold
        }
    )

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
        correlation_matrix.loc[name2, name1] = _cramers_corrected_stat(
            confusion_matrix, correction=True
        )
        correlation_matrix.loc[name1, name2] = correlation_matrix.loc[name2, name1]
    return correlation_matrix


@PhiK.compute.register(Settings, pd.DataFrame, dict)
def pandas_phik_compute(
    config: Settings, df: pd.DataFrame, summary: dict
) -> Optional[pd.DataFrame]:
    df_cols_dict = {i: list(df.columns).index(i) for i in df.columns}

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
        if value["type"] != "Unsupported"
        and 1 < value["n_distinct"] <= config.categorical_maximum_correlation_distinct
    }
    selcols = selcols.union(intcols)
    selected_cols = sorted(selcols, key=lambda i: df_cols_dict[i])

    if len(selected_cols) <= 1:
        return None

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        from phik import phik_matrix

        correlation = phik_matrix(df[selected_cols], interval_cols=list(intcols))

    return correlation
