"""Correlations between variables."""
import itertools
import warnings

import pandas as pd

from pandas_profiling.config import config
from pandas_profiling.model.base import Variable


def calculate_correlations(df: pd.DataFrame) -> dict:
    """Calculate the correlation coefficients between variables for the correlation types selected in the config
    (pearson, spearman, kendall, Phi_k).

    Args:
        df: The DataFrame with variables.

    Returns:
        A dictionary containing the correlation matrices for each of the active correlation measures.
    """
    correlations = {}
    if config["correlations"]["pearson"]:
        correlation = df.corr(method="pearson")
        if len(correlation) > 0:
            correlations["pearson"] = correlation
    if config["correlations"]["spearman"]:
        correlation = df.corr(method="spearman")
        if len(correlation) > 0:
            correlations["spearman"] = correlation
    if config["correlations"]["kendall"]:
        correlation = df.corr(method="kendall")
        if len(correlation) > 0:
            correlations["kendall"] = correlation
    if config["correlations"]["phi_k"]:
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
                    elif df[col].nunique() < 100:
                        selcols.append(col)
                except TypeError:
                    continue
                except ValueError:
                    continue

            correlations["phi_k"] = df[selcols].phik_matrix(interval_cols=intcols)

    return correlations


def perform_check_correlation(df_correlation_pearson):
    """
    Check for highly correlated values in the pearson correlation matrix and if found, reject them.

    Args:
        df_correlation_pearson: The pearson correlation matrix for the DataFrame.

    Returns:
        The variables that are highly correlated.

    Notes:
        If x~y and y~z but not x~z, it would be better to delete only y
        Better way would be to find out which variable causes the highest increase in multicollinearity.
    """

    # TODO: find a more reliable way to find highly correlated variables, as corr(x,y) > 0.9 and corr(y,z) > 0.9 does
    #  not imply corr(x,z) > 0.9
    variables = {}
    corr = df_correlation_pearson.copy()

    correlation_overrides = config["correlation_overrides"].get(list)
    correlation_threshold = config["correlation_threshold"].get(float)

    for x, corr_x in corr.iterrows():
        if correlation_overrides and x in correlation_overrides:
            continue

        for y, corr in corr_x.iteritems():
            if x == y:
                break

            if corr > correlation_threshold:
                variables[x] = {
                    "type": Variable.S_TYPE_CORR,
                    "correlation_var": y,
                    "correlation": corr,
                }
    return variables


def perform_check_recoded(df: pd.DataFrame, types: dict) -> dict:
    """Check whether categorical variables are recoded (categorical version of correlation).

    Args:
        df: The DataFrame.
        types: A dict of types for each variable.

    Returns:
        The variables that are recoded.
    """
    variables = {}
    categorical_variables = [
        (name, data)
        for (name, data) in df.iteritems()
        if types[name] == Variable.TYPE_CAT
    ]
    correlation_overrides = config["correlation_overrides"].get(list)
    for (name1, data1), (name2, data2) in itertools.combinations(
        categorical_variables, 2
    ):
        if correlation_overrides and name1 in correlation_overrides:
            continue

        confusion_matrix = pd.crosstab(data1, data2)
        if confusion_matrix.values.diagonal().sum() == len(df):
            variables[name1] = {
                "type": Variable.S_TYPE_RECODED,
                "correlation_var": name2,
            }
    return variables
