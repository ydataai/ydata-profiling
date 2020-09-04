"""Correlations between variables."""
import itertools
import warnings
from contextlib import suppress
from functools import partial
from typing import Callable, Dict, List, Optional, Union

import numpy as np
import pandas as pd
from confuse import NotFoundError
from pandas.core.base import DataError
from scipy import stats

from pandas_profiling.config import config
from pandas_profiling.model.typeset import Categorical


def cramers_corrected_stat(confusion_matrix, correction: bool) -> float:
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
    r, k = confusion_matrix.shape

    # Deal with NaNs later on
    with np.errstate(divide="ignore", invalid="ignore"):
        phi2corr = max(0.0, phi2 - ((k - 1.0) * (r - 1.0)) / (n - 1.0))
        rcorr = r - ((r - 1.0) ** 2.0) / (n - 1.0)
        kcorr = k - ((k - 1.0) ** 2.0) / (n - 1.0)
        corr = np.sqrt(phi2corr / min((kcorr - 1.0), (rcorr - 1.0)))
    return corr


def cramers_matrix(df: pd.DataFrame, variables: dict):
    """Calculate the Cramer's V correlation matrix.

    Args:
        df: The pandas DataFrame.
        variables: A dict with column names mapped to variable type.

    Returns:
        A Cramer's V matrix for categorical variables.
    """
    return categorical_matrix(
        df, variables, partial(cramers_corrected_stat, correction=True)
    )


def categorical_matrix(
    df: pd.DataFrame, variables: dict, correlation_function: Callable
) -> Optional[pd.DataFrame]:
    """Calculate a correlation matrix for categorical variables.

    Args:
        df: The pandas DataFrame.
        variables: A dict with column names mapped to variable type.
        correlation_function: A function to calculate the correlation between two variables.

    Returns:
        A correlation matrix for categorical variables.
    """
    categoricals = {
        column_name: df[column_name]
        for column_name, variable_type in variables.items()
        if variable_type == Categorical
        # TODO: solve in type system
        and config["categorical_maximum_correlation_distinct"].get(int)
        >= df[column_name].nunique()
        > 1
    }

    if len(categoricals) <= 1:
        return None

    correlation_matrix = pd.DataFrame(
        np.ones((len(categoricals), len(categoricals))),
        index=categoricals.keys(),
        columns=categoricals.keys(),
    )

    for (name1, data1), (name2, data2) in itertools.combinations(
        categoricals.items(), 2
    ):
        confusion_matrix = pd.crosstab(data1, data2)
        correlation_matrix.loc[name2, name1] = correlation_matrix.loc[
            name1, name2
        ] = correlation_function(confusion_matrix)

    return correlation_matrix


def warn_correlation(correlation_name, error):
    warnings.warn(
        f"""There was an attempt to calculate the {correlation_name} correlation, but this failed.
To hide this warning, disable the calculation
(using `df.profile_report(correlations={{\"{correlation_name}\": {{\"calculate\": False}}}})`
If this is problematic for your use case, please report this as an issue:
https://github.com/pandas-profiling/pandas-profiling/issues
(include the error message: '{error}')"""
    )


def calculate_correlation(
    df: pd.DataFrame, variables: dict, correlation_name: str
) -> Union[pd.DataFrame, None]:
    """Calculate the correlation coefficients between variables for the correlation types selected in the config
    (pearson, spearman, kendall, phi_k, cramers).

    Args:
        variables: A dict with column names and variable types.
        df: The DataFrame with variables.
        correlation_name:

    Returns:
        The correlation matrices for the given correlation measures. Return None if correlation is empty.
    """

    categorical_correlations = {"cramers": cramers_matrix}
    correlation = None

    if correlation_name in ["pearson", "spearman", "kendall"]:
        try:
            correlation = df.corr(method=correlation_name)

        except (ValueError, AssertionError, TypeError) as e:
            warn_correlation(correlation_name, e)
    elif correlation_name in ["phi_k"]:
        import phik

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            # Phi_k does not filter non-numerical with high cardinality
            selcols = []
            intcols = []
            for col in df.columns.tolist():
                try:
                    tmp = (
                        df[col]
                        .value_counts(dropna=False)
                        .reset_index()
                        .dropna()
                        .set_index("index")
                        .iloc[:, 0]
                    )
                    if tmp.index.inferred_type == "mixed":
                        continue

                    if pd.api.types.is_numeric_dtype(df[col]):
                        intcols.append(col)
                        selcols.append(col)
                    elif df[col].nunique() <= config[
                        "categorical_maximum_correlation_distinct"
                    ].get(int):
                        selcols.append(col)
                except (TypeError, ValueError):
                    continue

            if len(selcols) > 1:
                try:
                    correlation = df[selcols].phik_matrix(interval_cols=intcols)

                    # Only do this if the column_order is set
                    with suppress(NotFoundError):
                        # Get the preferred order
                        column_order = config["column_order"].get(list)

                        # Get the Phi_k sorted order
                        current_order = correlation.index.get_level_values(
                            "var1"
                        ).tolist()

                        # Intersection (some columns are not used in correlation)
                        column_order = [x for x in column_order if x in current_order]

                        # Override the Phi_k sorting
                        correlation = correlation.reindex(
                            index=column_order, columns=column_order
                        )
                except (ValueError, DataError, IndexError, TypeError) as e:
                    warn_correlation("phi_k", e)
    elif correlation_name in ["cramers"]:
        try:
            get_matrix = categorical_correlations[correlation_name]
            correlation = get_matrix(df, variables)
        except (ValueError, AssertionError) as e:
            warn_correlation(correlation_name, e)

    if correlation is None or len(correlation) <= 0:
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
