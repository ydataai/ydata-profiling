"""Correlations between variables."""
import itertools
import warnings
from typing import Optional

import numpy as np
import pandas as pd
from scipy import stats
from operator import add 
import pyspark
from pyspark import SparkContext, SparkConf
import numpy as np 
from collections import defaultdict

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

        appName = "test"
        master = "local"

        conf = SparkConf().setAppName(appName).setMaster(master)
        sc = SparkContext.getOrCreate(conf=conf)
        #zip sample data and convert to rdd
        def correlation_kendal(var1,var2):
            example_data = zip(var1, var2)
            example_rdd = sc.parallelize(example_data)
            #filer out all your null values. Row containing nulls will be removed
            example_rdd = example_rdd.filter(lambda x: x is not None).filter(lambda x: x != "")

            #take the cartesian product of example data (generate all possible combinations)
            all_pairs = example_rdd.cartesian(example_rdd)

            #function calculating concorant and disconordant pairs
            def calc(pair):
                p1, p2 = pair
                x1, y1 = p1
                x2, y2 = p2
                if (x1 == x2) and (y1 == y2):
                    return ("t", 1) #tie
                elif x1 == x2:
                    return ("xtie", 1) #tie
                elif y1 == y2:
                    return ("ytie", 1) #tie
                elif ((x1 > x2) and (y1 > y2)) or ((x1 < x2) and (y1 < y2)):
                    return ("c", 1) #concordant pair
                else:
                    return ("d", 1) #discordant pair

            #rank all pairs and calculate concordant / disconrdant pairs with calc() then return results
            results  = all_pairs.map(calc)

            #aggregate the results
            results = results.aggregateByKey(0, add, add)

            #count and collect
            try:
                d = {k: v for (k, v) in results.collect()}
                c_val = 0 if d.get("c") == None else d.get("c")
                d_val = 0 if d.get("d") == None else d.get("d")
                x_tie = 0 if d.get("xtie") == None else d.get("xtie")
                y_tie = 0 if d.get("ytie") == None else d.get("ytie")
                tau = (c_val - d_val) / ((c_val + d_val + x_tie) * (c_val + d_val + y_tie))**0.5
                tau=np.round(tau,decimals=6)
                return tau
            except Exception as e:
                raise e
        mapping_col_dict = defaultdict(list)
        for column1 in df.columns:
            for column2 in df.columns:
                    mapping_col_dict[column1].append(correlation_kendal(df[column1],df[column2]))
        output_df=pd.DataFrame.from_dict(mapping_col_dict)
        output_df.index=output_df.columns

        return output_df



    #return df.corr(method="kendall")


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
