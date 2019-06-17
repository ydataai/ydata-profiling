"""Correlations between variables."""
import itertools
import warnings
from functools import partial

import pandas as pd
import numpy as np
from scipy import stats

from pandas_profiling.config import config
from pandas_profiling.model.base import Variable


def cramers_corrected_stat(confusion_matrix, correction: bool) -> float:
    """Calculate the Cramers V corrected stat for two variables.

    Args:
        confusion_matrix: Crosstab between two variables.
        correction: Should the correction be applied?

    Returns:
        The Cramers V corrected stat for the two variables.
    """
    chi2 = stats.chi2_contingency(confusion_matrix, correction=correction)[0]
    n = confusion_matrix.sum().sum()
    phi2 = chi2 / n
    r, k = confusion_matrix.shape
    phi2corr = max(0.0, phi2 - ((k - 1.0) * (r - 1.0)) / (n - 1.0))
    rcorr = r - ((r - 1.0) ** 2.0) / (n - 1.0)
    kcorr = k - ((k - 1.0) ** 2.0) / (n - 1.0)
    return np.sqrt(phi2corr / min((kcorr - 1.0), (rcorr - 1.0)))


def check_recoded(confusion_matrix, count: int) -> int:
    """Check if two variables are recoded based on their crosstab.

    Args:
        confusion_matrix: Crosstab between two variables.
        count:  The number of variables.

    Returns:
        Whether the variables are recoded.
    """
    return int(confusion_matrix.values.diagonal().sum() == count)


def cramers_matrix(df: pd.DataFrame, variables: dict):
    """Calculate the Cramers v correlation matrix.

    Args:
        df: The pandas DataFrame.
        variables: A dict with column names mapped to variable type.

    Returns:
        A cramers v matrix for categorical variables.
    """
    return categorical_matrix(
        df, variables, partial(cramers_corrected_stat, correction=True)
    )


def recoded_matrix(df: pd.DataFrame, variables: dict):
    """Calculate the recoded correlation matrix.

    Args:
        df: The pandas DataFrame.
        variables: A dict with column names mapped to variable type.

    Returns:
        A recoded matrix for categorical variables.
    """
    return categorical_matrix(df, variables, partial(check_recoded, count=len(df)))


def categorical_matrix(
    df: pd.DataFrame, variables: dict, correlation_function: callable
):
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
        if variable_type == Variable.TYPE_CAT
        and df[column_name].nunique()
        <= config["categorical_maximum_correlation_distinct"].get(int)
    }

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


def calculate_correlations(df: pd.DataFrame, variables: dict) -> dict:
    """Calculate the correlation coefficients between variables for the correlation types selected in the config
    (pearson, spearman, kendall, Phi_k).

    Args:
        variables: A dict with column names and variable types.
        df: The DataFrame with variables.

    Returns:
        A dictionary containing the correlation matrices for each of the active correlation measures.
    """
    correlations = {}
    if config["correlations"]["pearson"].get(bool):
        correlation = df.corr(method="pearson")
        if len(correlation) > 0:
            correlations["pearson"] = correlation

    if config["correlations"]["spearman"].get(bool):
        correlation = df.corr(method="spearman")
        if len(correlation) > 0:
            correlations["spearman"] = correlation

    if config["correlations"]["kendall"].get(bool):
        correlation = df.corr(method="kendall")
        if len(correlation) > 0:
            correlations["kendall"] = correlation

    if config["correlations"]["phi_k"].get(bool):
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
                except TypeError:
                    continue
                except ValueError:
                    continue

            correlations["phi_k"] = df[selcols].phik_matrix(interval_cols=intcols)

    if config["correlations"]["cramers"].get(bool):
        correlation = cramers_matrix(df, variables)
        if len(correlation) > 0:
            correlations["cramers"] = correlation

    if config["correlations"]["recoded"].get(bool):
        correlation = recoded_matrix(df, variables)
        if len(correlation) > 0:
            correlations["recoded"] = correlation

    return correlations


def perform_check_correlation(
    correlation_matrix, criterion: callable, special_type: Variable
):
    """Check whether selected variables are highly correlated values in the correlation matrix and if found, reject them.

    Args:
        correlation_matrix: The correlation matrix for the DataFrame.
        criterion: a mapping function from the correlation function to a bool
        special_type: which type to return when the criterion is True (CORR, RECODED).

    Returns:
        The variables that are highly correlated or recoded.

    Notes:
        If x~y and y~z but not x~z, it would be better to delete only y
        Better way would be to find out which variable causes the highest increase in multicollinearity.
    """

    # TODO: find a more reliable way to find highly correlated variables, as corr(x,y) > 0.9 and corr(y,z) > 0.9 does
    #  not imply corr(x,z) > 0.9
    variables = {}
    corr = correlation_matrix.copy()

    correlation_overrides = config["correlation_overrides"].get(list)

    for x, corr_x in corr.iterrows():
        if correlation_overrides and x in correlation_overrides:
            continue

        for y, corr in corr_x.iteritems():
            if x == y:
                break

            if criterion(corr):
                variables[x] = {
                    "type": special_type,
                    "correlation_var": y,
                    "correlation": corr,
                }
    return variables
