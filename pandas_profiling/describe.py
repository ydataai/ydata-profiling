# -*- coding: utf-8 -*-
from pandas_profiling.plot import histogram, mini_histogram
import numpy as np
import pandas as pd
import matplotlib
from pandas_profiling.base import get_vartype
import pandas_profiling.formatters as formatters
import six
import multiprocessing
import itertools
from pkg_resources import resource_filename
from functools import partial

def pretty_name(x):
    x *= 100
    if x == int(x):
        return '%.0f%%' % x
    else:
        return '%.1f%%' % x

def describe_numeric_1d(series, **kwargs):
    stats = {'mean': series.mean(), 'std': series.std(), 'variance': series.var(), 'min': series.min(),
            'max': series.max()}
    stats['range'] = stats['max'] - stats['min']

    for x in np.array([0.05, 0.25, 0.5, 0.75, 0.95]):
        stats[pretty_name(x)] = series.dropna().quantile(x) # The dropna() is a workaround for https://github.com/pydata/pandas/issues/13098
    stats['iqr'] = stats['75%'] - stats['25%']
    stats['kurtosis'] = series.kurt()
    stats['skewness'] = series.skew()
    stats['sum'] = series.sum()
    stats['mad'] = series.mad()
    stats['cv'] = stats['std'] / stats['mean'] if stats['mean'] else np.NaN
    stats['type'] = "NUM"
    stats['n_zeros'] = (len(series) - np.count_nonzero(series))
    stats['p_zeros'] = stats['n_zeros'] / len(series)
    # Histograms
    stats['histogram'] = histogram(series, **kwargs)
    stats['mini_histogram'] = mini_histogram(series, **kwargs)
    return pd.Series(stats, name=series.name)


def describe_date_1d(series):
    stats = {'min': series.min(), 'max': series.max()}
    stats['range'] = stats['max'] - stats['min']
    stats['type'] = "DATE"
    stats['histogram'] = histogram(series)
    stats['mini_histogram'] = mini_histogram(series)
    return pd.Series(stats, name=series.name)


def describe_categorical_1d(data):
    # Only run if at least 1 non-missing value
    objcounts = data.value_counts()
    top, freq = objcounts.index[0], objcounts.iloc[0]
    names = []
    result = []

    if get_vartype(data) == 'CAT':
        names += ['top', 'freq', 'type']
        result += [top, freq, 'CAT']

    return pd.Series(result, index=names, name=data.name)

def describe_boolean_1d(data):
    objcounts = data.value_counts()
    top, freq = objcounts.index[0], objcounts.iloc[0]
    # The mean of boolean is an interesting information
    mean = data.mean()
    names = []
    result = []
    names += ['top', 'freq', 'type', 'mean']
    result += [top, freq, 'BOOL', mean]

    return pd.Series(result, index=names, name=data.name)

def describe_constant_1d(data):
    return pd.Series(['CONST'], index=['type'], name=data.name)


def describe_unique_1d(data):
    return pd.Series(['UNIQUE'], index=['type'], name=data.name)


def describe_1d(data, **kwargs):
    leng = len(data)  # number of observations in the Series
    count = data.count()  # number of non-NaN observations in the Series

    # Replace infinite values with NaNs to avoid issues with
    # histograms later.
    data.replace(to_replace=[np.inf, np.NINF, np.PINF], value=np.nan, inplace=True)

    n_infinite = count - data.count()  # number of infinte observations in the Series

    distinct_count = data.nunique(dropna=False)  # number of unique elements in the Series
    if count > distinct_count > 1:
        mode = data.mode().iloc[0]
    else:
        mode = data[0]

    results_data = {'count': count,
                    'distinct_count': distinct_count,
                    'p_missing': 1 - count / leng,
                    'n_missing': leng - count,
                    'p_infinite': n_infinite / leng,
                    'n_infinite': n_infinite,
                    'is_unique': distinct_count == leng,
                    'mode': mode,
                    'p_unique': distinct_count / leng}
    try:
        # pandas 0.17 onwards
        results_data['memorysize'] = data.memory_usage()
    except:
        results_data['memorysize'] = 0

    result = pd.Series(results_data, name=data.name)

    vartype = get_vartype(data)
    if vartype == 'CONST':
        result = result.append(describe_constant_1d(data))
    elif vartype == 'BOOL':
        result = result.append(describe_boolean_1d(data, **kwargs))
    elif vartype == 'NUM':
        result = result.append(describe_numeric_1d(data, **kwargs))
    elif vartype == 'DATE':
        result = result.append(describe_date_1d(data, **kwargs))
    elif vartype == 'UNIQUE':
        result = result.append(describe_unique_1d(data, **kwargs))
    else:
        result = result.append(describe_categorical_1d(data))
    return result


def multiprocess_func(x, **kwargs):
    return x[0], describe_1d(x[1], **kwargs)


def describe(df, bins=10, check_correlation=True, correlation_overrides=None, pool_size=multiprocessing.cpu_count(), **kwargs):
    """
    Generates a object containing summary statistics for a given DataFrame
    :param df: DataFrame to be analyzed
    :param bins: Number of bins in histogram
    :param check_correlation: Flag, set to False to skip correlation checks.
    :param correlation_overrides: Variable names not to be rejected because they are correlated
    :param pool_size: Number of workers in thread pool
    :return: Dictionary containing
        table: general statistics on the DataFrame
        variables: summary statistics for each variable
        freq: frequency table
    """

    if not isinstance(df, pd.DataFrame):
        raise TypeError("df must be of type pandas.DataFrame")
    if df.empty:
        raise ValueError("df can not be empty")

    try:
        # reset matplotlib style before use
        # Fails in matplotlib 1.4.x so plot might look bad
        matplotlib.style.use("default")
    except:
        pass

    matplotlib.style.use(resource_filename(__name__, "pandas_profiling.mplstyle"))

    if not pd.Index(np.arange(0, len(df))).equals(df.index):
        # Treat index as any other column
        df = df.reset_index()

    # Describe all variables in a univariate way
    pool = multiprocessing.Pool(pool_size)
    local_multiprocess_func = partial(multiprocess_func, **kwargs)
    ldesc = {col: s for col, s in pool.map(local_multiprocess_func, df.iteritems())}
    pool.close()

    # Check correlations between variable
    if check_correlation is True:
        ''' TODO: corr(x,y) > 0.9 and corr(y,z) > 0.9 does not imply corr(x,z) > 0.9
        If x~y and y~z but not x~z, it would be better to delete only y
        Better way would be to find out which variable causes the highest increase in multicollinearity.
        '''
        corr = df.corr()
        for x, corr_x in corr.iterrows():
            if correlation_overrides and x in correlation_overrides:
                continue

            for y, corr in corr_x.iteritems():
                if x == y: break

                if corr > 0.9:
                    ldesc[x] = pd.Series(['CORR', y, corr], index=['type', 'correlation_var', 'correlation'])

        categorical_variables = [(name, data) for (name, data) in df.iteritems() if get_vartype(data)=='CAT']
        for (name1, data1), (name2, data2) in itertools.combinations(categorical_variables, 2):
            if correlation_overrides and name1 in correlation_overrides:
                continue

            confusion_matrix=pd.crosstab(data1,data2)
            if confusion_matrix.values.diagonal().sum() == len(df):
                ldesc[name1] = pd.Series(['RECODED', name2], index=['type', 'correlation_var'])

    # Convert ldesc to a DataFrame
    names = []
    ldesc_indexes = sorted([x.index for x in ldesc.values()], key=len)
    for idxnames in ldesc_indexes:
        for name in idxnames:
            if name not in names:
                names.append(name)
    variable_stats = pd.concat(ldesc, join_axes=pd.Index([names]), axis=1)
    variable_stats.columns.names = df.columns.names

    # General statistics
    table_stats = {'n': len(df), 'nvar': len(df.columns)}
    table_stats['total_missing'] = variable_stats.loc['n_missing'].sum() / (table_stats['n'] * table_stats['nvar'])
    table_stats['n_duplicates'] = sum(df.duplicated())

    memsize = df.memory_usage(index=True).sum()
    table_stats['memsize'] = formatters.fmt_bytesize(memsize)
    table_stats['recordsize'] = formatters.fmt_bytesize(memsize / table_stats['n'])

    table_stats.update({k: 0 for k in ("NUM", "DATE", "CONST", "CAT", "UNIQUE", "CORR", "RECODED", "BOOL")})
    table_stats.update(dict(variable_stats.loc['type'].value_counts()))
    table_stats['REJECTED'] = table_stats['CONST'] + table_stats['CORR'] + table_stats['RECODED']

    return {'table': table_stats, 'variables': variable_stats.T, 'freq': {k: df[k].value_counts() for k in df.columns}}
