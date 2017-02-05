from __future__ import division

import sys

import itertools

try:
    from StringIO import BytesIO
except ImportError:
    from io import BytesIO

try:
    from urllib import quote
except ImportError:
    from urllib.parse import quote

import base64

import matplotlib
matplotlib.use('Agg')

import numpy as np
import pandas as pd
import pandas_profiling.formatters as formatters, pandas_profiling.templates as templates
from matplotlib import pyplot as plt
from pkg_resources import resource_filename
import six
import multiprocessing
from functools import partial
from distutils.version import LooseVersion


def pretty_name(x):
    x *= 100
    if x == int(x):
        return '%.0f%%' % x
    else:
        return '%.1f%%' % x


def get_vartype(data):
    distinct_count=data.nunique(dropna=False)
    leng=len(data)
    if distinct_count <=1:
        return 'CONST'
    elif pd.api.types.is_numeric_dtype(data):
        return 'NUM'
    elif pd.api.types.is_datetime64_dtype(data):
        return 'DATE'
    elif distinct_count==leng:
        return 'UNIQUE'
    else:
        return 'CAT'


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


def _plot_histogram(series, bins=10, figsize=(6, 4), facecolor='#337ab7'):
    """Plot an histogram from the data and return the AxesSubplot object.

    Parameters
    ----------
    series: Series, default None
        The data to plot
    figsize: a tuple (width, height) in inches, default (6,4)
        The size of the figure.
    facecolor: str
        The color code.

    Returns
    -------
    matplotlib.AxesSubplot, The plot.
    """
    if get_vartype(series) == 'DATE':
        # TODO: These calls should be merged
        fig = plt.figure(figsize=figsize)
        plot = fig.add_subplot(111)
        plot.set_ylabel('Frequency')
        try:
            plot.hist(series.values, facecolor=facecolor, bins=bins)
        except TypeError: # matplotlib 1.4 can't plot dates so will show empty plot instead
            pass
    else:
        plot = series.plot(kind='hist', figsize=figsize,
                           facecolor=facecolor,
                           bins=bins)  # TODO when running on server, send this off to a different thread
    return plot


def histogram(series, **kwargs):
    """Plot an histogram of the data.

    Parameters
    ----------
    series: Series, default None
        The data to plot.

    Returns
    -------
    str, The resulting image encoded as a string.
    """
    imgdata = BytesIO()
    plot = _plot_histogram(series, **kwargs)
    plot.figure.subplots_adjust(left=0.15, right=0.95, top=0.9, bottom=0.1, wspace=0, hspace=0)
    plot.figure.savefig(imgdata)
    imgdata.seek(0)
    result_string = 'data:image/png;base64,' + quote(base64.b64encode(imgdata.getvalue()))
    # TODO Think about writing this to disk instead of caching them in strings
    plt.close(plot.figure)
    return result_string


def mini_histogram(series, **kwargs):
    """Plot a small (mini) histogram of the data.

    Parameters
    ----------
    series: Series, default None
        The data to plot.

    Returns
    -------
    str, The resulting image encoded as a string.
    """
    imgdata = BytesIO()
    plot = _plot_histogram(series, figsize=(2, 0.75), **kwargs)
    plot.axes.get_yaxis().set_visible(False)

    if LooseVersion(matplotlib.__version__) <= '1.5.9':
        plot.set_axis_bgcolor("w")
    else:
        plot.set_facecolor("w")

    xticks = plot.xaxis.get_major_ticks()
    for tick in xticks[1:-1]:
        tick.set_visible(False)
        tick.label.set_visible(False)
    for tick in (xticks[0], xticks[-1]):
        tick.label.set_fontsize(8)
    plot.figure.subplots_adjust(left=0.15, right=0.85, top=1, bottom=0.35, wspace=0, hspace=0)
    plot.figure.savefig(imgdata)
    imgdata.seek(0)
    result_string = 'data:image/png;base64,' + quote(base64.b64encode(imgdata.getvalue()))
    plt.close(plot.figure)
    return result_string


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
                    'p_unique': distinct_count / count}
    try:
        # pandas 0.17 onwards
        results_data['memorysize'] = data.memory_usage()
    except:
        results_data['memorysize'] = 0

    result = pd.Series(results_data, name=data.name)

    vartype = get_vartype(data)
    if vartype == 'CONST':
        result = result.append(describe_constant_1d(data))
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


def describe(df, bins=10, correlation_overrides=None, pool_size=multiprocessing.cpu_count(), **kwargs):
    """
    Generates a object containing summary statistics for a given DataFrame
    :param df: DataFrame to be analyzed
    :param bins: Number of bins in histogram
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

    # Check correlations between variables
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

    table_stats.update({k: 0 for k in ("NUM", "DATE", "CONST", "CAT", "UNIQUE", "CORR", "RECODED")})
    table_stats.update(dict(variable_stats.loc['type'].value_counts()))
    table_stats['REJECTED'] = table_stats['CONST'] + table_stats['CORR'] + table_stats['RECODED']

    return {'table': table_stats, 'variables': variable_stats.T, 'freq': {k: df[k].value_counts() for k in df.columns}}


def to_html(sample, stats_object):
    """Generate a HTML report from summary statistics and a given sample.

    Parameters
    ----------
    sample: DataFrame containing the sample you want to print
    stats_object: Dictionary containing summary statistics. Should be generated with an appropriate describe() function

    Returns
    -------
    str, containing profile report in HTML format
    """

    n_obs = stats_object['table']['n']

    value_formatters = formatters.value_formatters
    row_formatters = formatters.row_formatters

    if not isinstance(sample, pd.DataFrame):
        raise TypeError("sample must be of type pandas.DataFrame")

    if not isinstance(stats_object, dict):
        raise TypeError("stats_object must be of type dict. Did you generate this using the pandas_profiling.describe() function?")

    if set(stats_object.keys()) != {'table', 'variables', 'freq'}:
        raise TypeError("stats_object badly formatted. Did you generate this using the pandas_profiling-eda.describe() function?")

    def fmt(value, name):
        if pd.isnull(value):
            return ""
        if name in value_formatters:
            return value_formatters[name](value)
        elif isinstance(value, float):
            return value_formatters[formatters.DEFAULT_FLOAT_FORMATTER](value)
        else:
            if sys.version_info.major == 3:
                return str(value)
            else:
                return unicode(value)

    def _format_row(freq, label, max_freq, row_template, n, extra_class=''):
            width = int(freq / max_freq * 99) + 1
            if width > 20:
                label_in_bar = freq
                label_after_bar = ""
            else:
                label_in_bar = "&nbsp;"
                label_after_bar = freq

            return row_template.render(label=label,
                                       width=width,
                                       count=freq,
                                       percentage='{:2.1f}'.format(freq / n * 100),
                                       extra_class=extra_class,
                                       label_in_bar=label_in_bar,
                                       label_after_bar=label_after_bar)

    def freq_table(freqtable, n, table_template, row_template, max_number_to_print):

        freq_rows_html = u''

        if max_number_to_print > n:
                max_number_to_print=n

        if max_number_to_print < len(freqtable):
            freq_other = sum(freqtable.iloc[max_number_to_print:])
            min_freq = freqtable.values[max_number_to_print]
        else:
            freq_other = 0
            min_freq = 0

        freq_missing = n - sum(freqtable)
        max_freq = max(freqtable.values[0], freq_other, freq_missing)

        # TODO: Correctly sort missing and other

        for label, freq in six.iteritems(freqtable.iloc[0:max_number_to_print]):
            freq_rows_html += _format_row(freq, label, max_freq, row_template, n)

        if freq_other > min_freq:
            freq_rows_html += _format_row(freq_other,
                                         "Other values (%s)" % (freqtable.count() - max_number_to_print), max_freq, row_template, n,
                                         extra_class='other')

        if freq_missing > min_freq:
            freq_rows_html += _format_row(freq_missing, "(Missing)", max_freq, row_template, n, extra_class='missing')

        return table_template.render(rows=freq_rows_html, varid=hash(idx))

    def extreme_obs_table(freqtable, table_template, row_template, number_to_print, n, ascending = True):
        if ascending:
            obs_to_print = freqtable.sort_index().iloc[:number_to_print]
        else:
            obs_to_print = freqtable.sort_index().iloc[-number_to_print:]

        freq_rows_html = ''
        max_freq = max(obs_to_print.values)

        for label, freq in six.iteritems(obs_to_print):
            freq_rows_html += _format_row(freq, label, max_freq, row_template, n)

        return table_template.render(rows=freq_rows_html)

    # Variables
    rows_html = u""
    messages = []

    for idx, row in stats_object['variables'].iterrows():

        formatted_values = {'varname': idx, 'varid': hash(idx)}
        row_classes = {}

        for col, value in six.iteritems(row):
            formatted_values[col] = fmt(value, col)

        for col in set(row.index) & six.viewkeys(row_formatters):
            row_classes[col] = row_formatters[col](row[col])
            if row_classes[col] == "alert" and col in templates.messages:
                messages.append(templates.messages[col].format(formatted_values, varname = formatters.fmt_varname(idx)))

        if row['type'] == 'CAT':
            formatted_values['minifreqtable'] = freq_table(stats_object['freq'][idx], n_obs,
                                                           templates.template('mini_freq_table'), templates.template('mini_freq_table_row'), 3)

            if row['distinct_count'] > 50:
                messages.append(templates.messages['HIGH_CARDINALITY'].format(formatted_values, varname = formatters.fmt_varname(idx)))
                row_classes['distinct_count'] = "alert"
            else:
                row_classes['distinct_count'] = ""

        if row['type'] == 'UNIQUE':
            obs = stats_object['freq'][idx].index

            formatted_values['firstn'] = pd.DataFrame(obs[0:3], columns=["First 3 values"]).to_html(classes="example_values", index=False)
            formatted_values['lastn'] = pd.DataFrame(obs[-3:], columns=["Last 3 values"]).to_html(classes="example_values", index=False)

        if row['type'] in {'CORR', 'CONST', 'RECODED'}:
            formatted_values['varname'] = formatters.fmt_varname(idx)
            messages.append(templates.messages[row['type']].format(formatted_values))
        else:
            formatted_values['freqtable'] = freq_table(stats_object['freq'][idx], n_obs,
                                                       templates.template('freq_table'), templates.template('freq_table_row'), 10)
            formatted_values['firstn_expanded'] = extreme_obs_table(stats_object['freq'][idx], templates.template('freq_table'), templates.template('freq_table_row'), 5, n_obs, ascending = True)
            formatted_values['lastn_expanded'] = extreme_obs_table(stats_object['freq'][idx], templates.template('freq_table'), templates.template('freq_table_row'), 5, n_obs, ascending = False)

        rows_html += templates.row_templates_dict[row['type']].render(values=formatted_values, row_classes=row_classes)

    # Overview
    formatted_values = {k: fmt(v, k) for k, v in six.iteritems(stats_object['table'])}

    row_classes={}
    for col in six.viewkeys(stats_object['table']) & six.viewkeys(row_formatters):
        row_classes[col] = row_formatters[col](stats_object['table'][col])
        if row_classes[col] == "alert" and col in templates.messages:
            messages.append(templates.messages[col].format(formatted_values, varname = formatters.fmt_varname(idx)))

    messages_html = u''
    for msg in messages:
        messages_html += templates.message_row.format(message=msg)

    overview_html = templates.template('overview').render(values=formatted_values, row_classes = row_classes, messages=messages_html)

    # Sample

    sample_html = templates.template('sample').render(sample_table_html=sample.to_html(classes="sample"))
    # TODO: should be done in the template
    return templates.template('base').render({'overview_html': overview_html, 'rows_html': rows_html, 'sample_html': sample_html})
