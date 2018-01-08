import scipy.stats as stats
import itertools
import numpy as np
import pandas as pd

def cramers_corrected_stat(confusion_matrix, correction):
    chi2 = stats.chi2_contingency(confusion_matrix, correction=correction)[0]
    n = confusion_matrix.sum().sum()
    phi2 = chi2 / n
    r, k = confusion_matrix.shape
    phi2corr = max(0, phi2 - ((k - 1) * (r - 1)) / (n - 1))
    rcorr = r - ((r - 1) ** 2) / (n - 1)
    kcorr = k - ((k - 1) ** 2) / (n - 1)
    return np.sqrt(phi2corr / min((kcorr - 1), (rcorr - 1)))

def pearson_corr(df, exclude=[]):
    if exclude:
        cols = [col for col in df.columns if col not in exclude]
        filtered_df = df[cols]
    else:
        filtered_df = df
    return filtered_df.corr(method="pearson")


def spearman_cor(df, exclude=[]):
    if exclude:
        cols = [col for col in df.columns if col not in exclude]
        filtered_df = df[cols]
    else:
        filtered_df = df
    return filtered_df.corr(method="spearman")


def cramers_corr(df, exclude=[]):
    return create_corr(df, lambda cm: cramers_corrected_stat(cm, True),
                       lambda base: np.ones((base, base)), exclude=exclude)


def recoded_corr(df, exclude=[]):
    return create_corr(df, lambda cm: cm.values.diagonal().sum() == len(df),
                       lambda base: np.full((base, base), True), exclude=exclude)


def create_corr(df, corr_func, filler, exclude=[]):
    import pandas_profiling.base as base
    categorical_variables = [(name, data) for (name, data) in df.iteritems() if base.get_vartype(data) == 'CAT']
    column_names = [tuple[0] for tuple in categorical_variables]
    base = len(column_names)
    correlation_matrix = pd.DataFrame(filler(base), index=column_names, columns=column_names)
    for (name1, data1), (name2, data2) in itertools.combinations(categorical_variables, 2):
        if name1 in exclude:
            continue

        confusion_matrix = pd.crosstab(data1, data2)
        correlation_matrix.loc[name1, name2] = corr_func(confusion_matrix)
        correlation_matrix.loc[name2, name1] = correlation_matrix.loc[name1, name2]
    return correlation_matrix


def overthreshold_corr(corr, type, threshold_func):
    overthreshold = {}
    for x, corr_x in corr.iterrows():
        for y, corr in corr_x.iteritems():
            if x == y: break

            if threshold_func(corr):
                overthreshold[x] = (pd.Series([type, y, corr], index=['type', 'correlation_var', 'correlation']))
    return overthreshold