# -*- coding: utf-8 -*-
"""Compute statistical description of datasets"""
import multiprocessing
import itertools
from functools import partial
import numpy as np
import pandas as pd
import scipy as sp
import dask.dataframe as dd
from dask import delayed, compute
from dask.array import stats as dask_stats
import matplotlib
from pkg_resources import resource_filename
import dask_profiling.formatters as formatters
import dask_profiling.base as base
from dask_profiling.plot import histogram, mini_histogram

def describe_numeric_1d(series, **kwargs):
    """Compute summary statistics of a numerical (`TYPE_NUM`) variable (a Series).

    Also create histograms (mini an full) of its distribution.

    Parameters
    ----------
    series : Series
        The variable to describe.

    Returns
    -------
    Series
        The description of the variable as a Series with index being stats keys.
    """
    # Format a number as a percentage. For example 0.25 will be turned to 25%.
    _percentile_format = "{:.0%}"
    stats = dict()

    stats['type'] = base.TYPE_NUM
    stats['mean'] = series.mean()
    stats['std'] = series.std()
    stats['variance'] = series.var()
    stats['min'] = series.min()
    stats['max'] = series.max()
    stats['range'] = stats['max'] - stats['min']
    # TODO: Remove this "lazy" operation
    _series_no_na = series.dropna()
    for percentile in np.array([0.05, 0.25, 0.5, 0.75, 0.95]):
        # The dropna() is a workaround for https://github.com/pydata/pandas/issues/13098
        stats[_percentile_format.format(percentile)] = _series_no_na.quantile(percentile)
    stats['iqr'] = stats['75%'] - stats['25%']
    stats['kurtosis'] = delayed(sp.stats.kurtosis)(series)
    stats['skewness'] = delayed(float)(dask_stats.skew(series.to_dask_array()))
    stats['sum'] = series.sum()
    stats['mad'] = series.sub(series.mean()).abs().mean()
    # removed conditional for testing (no purpose was seen)
    # stats['cv'] = stats['std'] / stats['mean'] if stats['mean'] else np.NaN
    stats['cv'] = stats['std'] / stats['mean']
    stats['n_zeros'] = (series.size - delayed(np.count_nonzero)(series))
    stats['p_zeros'] = stats['n_zeros'] * 1.0 / series.size
    # Histograms
    # TODO: optimize histogram and mini_histogram calls (a big overlap in computation)
    stats['histogram'] = histogram(series, **kwargs)
    stats['mini_histogram'] = mini_histogram(series, **kwargs)

    return stats


def describe_date_1d(series):
    """Compute summary statistics of a date (`TYPE_DATE`) variable (a Series).

    Also create histograms (mini an full) of its distribution.

    Parameters
    ----------
    series : Series
        The variable to describe.

    Returns
    -------
    dict
        The description of the variable as a dict with keys being stats.
    """
    stats = dict()
    stats['type'] = base.TYPE_DATE
    stats['min'] = series.min()
    stats['max'] = series.max()
    stats['range'] = stats['max'] - stats['min']
    # Histograms
    # TODO: optimize histogram and mini_histogram calls (a big overlap in computation)
    stats['histogram'] = histogram(series)
    stats['mini_histogram'] = mini_histogram(series)
    
    return stats

def describe_categorical_1d(series):
    """Compute summary statistics of a categorical (`TYPE_CAT`) variable (a Series).

    Parameters
    ----------
    series : Series
        The variable to describe.

    Returns
    -------
    dict
        The description of the variable as a dict with keys being stats.
    """
    # Only run if at least 1 non-missing value
    value_counts, _ = base.get_groupby_statistic(series)
    top, freq = value_counts.index.head(1).values[0], value_counts.head(1).values[0]
    result = {
        'top': top,
        'freq': freq,
        'type': base.TYPE_CAT
    }

    return result

def describe_boolean_1d(series):
    """Compute summary statistics of a boolean (`TYPE_BOOL`) variable (a Series).

    Parameters
    ----------
    series : Series
        The variable to describe.

    Returns
    -------
    dict
        The description of the variable as a dict with keys being stats.
    """
    value_counts, distinct_count = base.get_groupby_statistic(series)
    value_counts = value_counts.compute()  # TODO: compare .compute() and .head()
    top, freq = value_counts.index[0], value_counts.iloc[0]
    # The mean of boolean is an interesting information
    mean = series.mean()
    result = {
        'top': top,
        'freq': freq,
        'type': base.TYPE_BOOL,
        'mean': mean
    }

    return result

def describe_constant_1d(series):
    """Compute summary statistics of a constant (`S_TYPE_CONST`) variable (a Series).

    Parameters
    ----------
    series : Series
        The variable to describe.

    Returns
    -------
    dict
        The description of the variable as a dict with keys being stats.
    """
    return {'type': base.S_TYPE_CONST}

def describe_unique_1d(series):
    """Compute summary statistics of a unique (`S_TYPE_UNIQUE`) variable (a Series).

    Parameters
    ----------
    series : Series
        The variable to describe.

    Returns
    -------
    dict
        The description of the variable as a dict with keys being stats.
    """
    return {'type': base.S_TYPE_UNIQUE}

def describe_supported(series, **kwargs):
    """Compute summary statistics of a supported variable (a Series).

    Parameters
    ----------
    series : Series
        The variable to describe.

    Returns
    -------
    dict
        The description of the variable as a dict with keys being stats.
    """
    leng = series.size  # number of observations in the Series
    count = series.count()  # number of non-NaN observations in the Series
    n_infinite = count - series.count()  # number of infinte observations in the Series

    value_counts, distinct_count = base.get_groupby_statistic(series)
    count, distinct_count = compute(count, distinct_count)
    # if all(compute(count > distinct_count, distinct_count > 1)): # Logical AND over the two comparisons
    if count > distinct_count > 1:
        mode = value_counts.index.head(1).values[0] # TODO: lazy mode
    else:
        mode = series.head(1, npartitions=-1).values[0]

    results_data = {'count': count,
                    'distinct_count': distinct_count,
                    'p_missing': 1 - count * 1.0 / leng,
                    'n_missing': leng - count,
                    'p_infinite': n_infinite * 1.0 / leng,
                    'n_infinite': n_infinite,
                    'is_unique': distinct_count == leng,
                    'mode': mode,
                    'p_unique': distinct_count * 1.0 / leng}
    try:
        # pandas 0.17 onwards
        results_data['memorysize'] = series.memory_usage()
    except:
        results_data['memorysize'] = 0

    return results_data

def describe_unsupported(series, **kwargs):
    """Compute summary statistics of a unsupported (`S_TYPE_UNSUPPORTED`) variable (a Series).

    Parameters
    ----------
    series : Series
        The variable to describe.

    Returns
    -------
    dict
        The description of the variable as a dict with keys being stats.
    """
    leng = series.size  # number of observations in the Series
    count = series.count()  # number of non-NaN observations in the Series
    n_infinite = count - series.count()  # number of infinte observations in the Series

    results_data = {'count': count,
                    'p_missing': 1 - count * 1.0 / leng,
                    'n_missing': leng - count,
                    'p_infinite': n_infinite * 1.0 / leng,
                    'n_infinite': n_infinite,
                    'type': base.S_TYPE_UNSUPPORTED}

    try:
        # pandas 0.17 onwards
        results_data['memorysize'] = series.memory_usage()
    except:
        results_data['memorysize'] = 0

    return results_data

def describe_1d(data, **kwargs):
    """Compute summary statistics of a variable (a Series).

    The description is different according to the type of the variable.
    However a set of common stats is also computed.

    Parameters
    ----------
    series : Series
        The variable to describe.

    Returns
    -------
    string
        The name of the variable (data).
    dict
        The description of the variable as a dict.
    """

    # Replace infinite values with NaNs to avoid issues with
    # histograms later.
    #data = data.replace(to_replace=[np.inf, np.NINF, np.PINF], value=np.nan)
    #data.map_partitions(pandas.DataFrame.replace, to_replace=[np.inf, np.NINF, np.PINF], value=np.nan)


    result = dict()

    vartype = base.get_vartype(data)

    if vartype == base.S_TYPE_UNSUPPORTED:
        result.update(describe_unsupported(data))
    else:
        result.update(describe_supported(data))

        if vartype == base.S_TYPE_CONST:
            result.update(describe_constant_1d(data))
        elif vartype == base.TYPE_BOOL:
            result.update(describe_boolean_1d(data))
        elif vartype == base.TYPE_NUM:
            result.update(describe_numeric_1d(data, **kwargs))
        elif vartype == base.TYPE_DATE:
            result.update(describe_date_1d(data))
        elif vartype == base.S_TYPE_UNIQUE:
            result.update(describe_unique_1d(data))
        else:
            # TYPE_CAT
            result.update(describe_categorical_1d(data))

    return data.name, result

def multiprocess_func(x, **kwargs):
    return x[0], describe_1d(x[1], **kwargs)

def describe(df, bins=10, check_correlation=True, correlation_threshold=0.9, correlation_overrides=None, check_recoded=False, pool_size=multiprocessing.cpu_count(), **kwargs):
    """Generates a dict containing summary statistics for a given dataset stored as a pandas `DataFrame`.

    Used has is it will output its content as an HTML report in a Jupyter notebook.

    Parameters
    ----------
    df : DataFrame
        Data to be analyzed
    bins : int
        Number of bins in histogram.
        The default is 10.
    check_correlation : boolean
        Whether or not to check correlation.
        It's `True` by default.
    correlation_threshold: float
        Threshold to determine if the variable pair is correlated.
        The default is 0.9.
    correlation_overrides : list
        Variable names not to be rejected because they are correlated.
        There is no variable in the list (`None`) by default.
    check_recoded : boolean
        Whether or not to check recoded correlation (memory heavy feature).
        Since it's an expensive computation it can be activated for small datasets.
        `check_correlation` must be true to disable this check.
        It's `False` by default.
    pool_size : int
        Number of workers in thread pool
        The default is equal to the number of CPU.

    Returns
    -------
    dict
        Containing the following keys:
            * table: general statistics on the dataset
            * variables: summary statistics for each variable
            * freq: frequency table

    Notes:
    ------
        * The section dedicated to check the correlation should be externalized
    """

    if not isinstance(df, dd.DataFrame):
        raise TypeError("df must be of type dask.dataframe.DataFrame")
    # too expensive. TODO: workaround
    # if (len(df) == 0):
    #     raise ValueError("df can not be empty")

    try:
        # reset matplotlib style before use
        # Fails in matplotlib 1.4.x so plot might look bad
        matplotlib.style.use("default")
    except:
        pass

    try:
        # Ignore FutureWarning
        from pandas.plotting import register_matplotlib_converters
        register_matplotlib_converters()
    except:
        pass

    matplotlib.style.use(resource_filename(__name__, "dask_profiling.mplstyle"))

    # Clearing the cache before computing stats
    base.clear_cache()

    # TODO: Improve this check, it'll take a LONG time this way
    # if not pd.Index(np.arange(0, len(df))).equals(df.index.compute()):
    #     # Treat index as any other column
    #     df = df.reset_index()
    df = df.reset_index()

    kwargs.update({'bins': bins})
    # Describe all variables in a univariate way
    # if pool_size == 1:
    #     local_multiprocess_func = partial(multiprocess_func, **kwargs)
    #     ldesc = {col: s for col, s in map(local_multiprocess_func, df.iteritems())}
    # else:
    #     pool = multiprocessing.Pool(pool_size)
    #     local_multiprocess_func = partial(multiprocess_func, **kwargs)
    #     ldesc = {col: s for col, s in pool.map(local_multiprocess_func, df.iteritems())}
    #     pool.close()

    ldesc = dict()
    for col in df.columns:
        _, desc = describe_1d(df[col])
        ldesc[col] = desc

    # Get correlations
    dfcorrPear = df.corr(method="pearson")
    # Spearman's correlation has not been implemented yet
    # dfcorrSpear = df.corr(method="spearman")

    # Check correlations between variable
    if check_correlation is True:
        ''' TODO: corr(x,y) > 0.9 and corr(y,z) > 0.9 does not imply corr(x,z) > 0.9
        If x~y and y~z but not x~z, it would be better to delete only y
        Better way would be to find out which variable causes the highest increase in multicollinearity.
        '''
        corr = dfcorrPear.copy()
        for x, corr_x in corr.iterrows():
            if correlation_overrides and x in correlation_overrides:
                continue

            for y, corr in corr_x.iteritems():
                if x == y: break

                if corr > correlation_threshold:
                    ldesc[x] = {
                        'type': 'CORR',
                        'correlation_var': y,
                        'correlation': corr
                    }

        # TODO:
        # if check_recoded:
        #     categorical_variables = [(name, data) for (name, data) in df.iteritems() if base.get_vartype(data)=='CAT']
        #     for (name1, data1), (name2, data2) in itertools.combinations(categorical_variables, 2):
        #         if correlation_overrides and name1 in correlation_overrides:
        #             continue

        #         confusion_matrix=pd.crosstab(data1,data2)
        #         if confusion_matrix.values.diagonal().sum() == len(df):
        #             ldesc[name1] = pd.Series(['RECODED', name2], index=['type', 'correlation_var'])

    # Convert ldesc to a DataFrame
    # TODO: Beautify, as above
    # names = []
    # ldesc_indexes = sorted([x.index for x in ldesc.values()], key=len)
    # for idxnames in ldesc_indexes:
    #     for name in idxnames:
    #         if name not in names:
    #             names.append(name)
    # variable_stats = pd.concat(ldesc, join_axes=pd.Index([names]), axis=1)
    # variable_stats.columns.names = df.columns.names
    variable_stats = pd.DataFrame.from_dict(compute(ldesc)[0])

    # General statistics
    table_stats = {}

    table_stats['n'] = delayed(len)(df)
    table_stats['nvar'] = delayed(len)(df.columns)
    table_stats['total_missing'] = variable_stats.loc['n_missing'].sum() / (table_stats['n'] * table_stats['nvar'])
    unsupported_columns = variable_stats.transpose()[variable_stats.transpose().type != base.S_TYPE_UNSUPPORTED].index.tolist()
    table_stats['n_duplicates'] = (delayed(len)(df[unsupported_columns].drop_duplicates()) - delayed(len)(df)) if len(unsupported_columns) > 0 else 0

    memsize = df.memory_usage(index=True).sum()
    table_stats, memsize = compute(table_stats, memsize)
    table_stats['memsize'] = formatters.fmt_bytesize(memsize)
    table_stats['recordsize'] = formatters.fmt_bytesize(memsize / table_stats['n'])

    table_stats.update({k: 0 for k in ("NUM", "DATE", "CONST", "CAT", "UNIQUE", "CORR", "RECODED", "BOOL", "UNSUPPORTED")})
    table_stats.update(dict(variable_stats.loc['type'].value_counts()))
    table_stats['REJECTED'] = table_stats['CONST'] + table_stats['CORR'] + table_stats['RECODED']

    return compute({
        'table': table_stats,
        'variables': variable_stats.T,
        'freq': {k: (base.get_groupby_statistic(df[k])[0] if variable_stats[k].type != base.S_TYPE_UNSUPPORTED else None) for k in df.columns},
        # 'correlations': {'pearson': dfcorrPear, 'spearman': dfcorrSpear}
        'correlations': {'pearson': dfcorrPear}
    })[0]
