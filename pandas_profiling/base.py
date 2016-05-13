from __future__ import division

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
import os
import pandas as pd
import pandas_profiling.formatters as formatters, pandas_profiling.templates as templates
from matplotlib import pyplot as plt
from pandas.core import common as com
import six
from pkg_resources import resource_filename


def describe(df, **kwargs):
    """
    Generates a object containing summary statistics for a given DataFrame
    :param df: DataFrame to be analyzed
    :param bins: Number of bins in histogram
    :return: Dictionary containing
        table: general statistics on the DataFrame
        variables: summary statistics for each variable
        freq: frequency table
    """

    if not isinstance(df, pd.DataFrame):
        raise TypeError("df must be of type pandas.DataFrame")
    if df.empty:
        raise ValueError("df can not be empty")

    bins = kwargs.get('bins', 10)

    try:
        # reset matplotlib style before use
        # Fails in matplotlib 1.4.x so plot might look bad
        matplotlib.style.use("default")
    except:
        pass

    matplotlib.style.use(resource_filename(__name__, "pandas_profiling.mplstyle"))

    def pretty_name(x):
        x *= 100
        if x == int(x):
            return '%.0f%%' % x
        else:
            return '%.1f%%' % x

    def describe_numeric_1d(series, base_stats):
        stats = {'mean': series.mean(), 'std': series.std(), 'variance': series.var(), 'min': series.min(),
                'max': series.max()}
        stats['range'] = stats['max'] - stats['min']

        for x in np.array([0.05, 0.25, 0.5, 0.75, 0.95]):
            stats[pretty_name(x)] = series.quantile(x)
        stats['iqr'] = stats['75%'] - stats['25%']
        stats['kurtosis'] = series.kurt()
        stats['skewness'] = series.skew()
        stats['sum'] = series.sum()
        stats['mad'] = series.mad()
        stats['cv'] = stats['std'] / stats['mean'] if stats['mean'] else np.NaN
        stats['type'] = "NUM"
        stats['n_zeros'] = (len(series) - np.count_nonzero(series))
        stats['p_zeros'] = stats['n_zeros'] / len(series)

        # Large histogram
        imgdata = BytesIO()
        plot = series.plot(kind='hist', figsize=(6, 4),
                           facecolor='#337ab7', bins=bins)  # TODO when running on server, send this off to a different thread
        plot.figure.subplots_adjust(left=0.15, right=0.95, top=0.9, bottom=0.1, wspace=0, hspace=0)
        plot.figure.savefig(imgdata)
        imgdata.seek(0)
        stats['histogram'] = 'data:image/png;base64,' + quote(base64.b64encode(imgdata.getvalue()))
        #TODO Think about writing this to disk instead of caching them in strings
        plt.close(plot.figure)

        stats['mini_histogram'] = mini_histogram(series)

        return pd.Series(stats, name=series.name)

    def mini_histogram(series):
        # Small histogram
        imgdata = BytesIO()
        plot = series.plot(kind='hist', figsize=(2, 0.75), facecolor='#337ab7', bins=bins)
        plot.axes.get_yaxis().set_visible(False)
        plot.set_axis_bgcolor("w")
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

    def describe_date_1d(series, base_stats):
        stats = {'min': series.min(), 'max': series.max()}
        stats['range'] = stats['max'] - stats['min']
        stats['type'] = "DATE"

        # TODO: Matplotlib can't do histograms of dates.
        # stats['mini_histogram'] = mini_histogram(series)

        return pd.Series(stats, name=series.name)

    def describe_categorical_1d(data):
        # Only run if at least 1 non-missing value
        objcounts = data.value_counts()
        top, freq = objcounts.index[0], objcounts.iloc[0]
        names = []
        result = []

        if data.dtype == object or com.is_categorical_dtype(data.dtype):
            names += ['top', 'freq', 'type']
            result += [top, freq, 'CAT']

        return pd.Series(result, index=names, name=data.name)

    def describe_constant_1d(data):
        return pd.Series(['CONST'], index=['type'], name=data.name)

    def describe_unique_1d(data):
        return pd.Series(['UNIQUE'], index=['type'], name=data.name)

    def describe_1d(data):
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

        if distinct_count <= 1:
            result = result.append(describe_constant_1d(data))
        elif com.is_numeric_dtype(data):
            result = result.append(describe_numeric_1d(data, result))
        elif com.is_datetime64_dtype(data):
            result = result.append(describe_date_1d(data, result))
        elif distinct_count == leng:
            result = result.append(describe_unique_1d(data))
        else:
            result = result.append(describe_categorical_1d(data))
        return result

    if not pd.Index(np.arange(0, len(df))).equals(df.index):
        # Treat index as any other column
        df = df.reset_index()

    # Describe all variables in a univariate way
    ldesc = {col: describe_1d(s) for col, s in df.iteritems()}

    # Check correlations between variables
    ''' TODO: corr(x,y) > 0.9 and corr(y,z) > 0.9 does not imply corr(x,z) > 0.9
    If x~y and y~z but not x~z, it would be better to delete only y
    Better way would be to find out which variable causes the highest increase in multicollinearity.
    '''
    corr = df.corr()
    for x, corr_x in corr.iterrows():
        for y, corr in corr_x.iteritems():
            if x == y: break

            if corr > 0.9:
                ldesc[x] = pd.Series(['CORR', y, corr], index=['type', 'correlation_var', 'correlation'], name=x)

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

    table_stats.update({k: 0 for k in ("NUM", "DATE", "CONST", "CAT", "UNIQUE", "CORR")})
    table_stats.update(dict(variable_stats.loc['type'].value_counts()))
    table_stats['REJECTED'] = table_stats['CONST'] + table_stats['CORR']

    return {'table': table_stats, 'variables': variable_stats.T, 'freq': {k: df[k].value_counts() for k in df.columns}}


def to_html(sample, stats_object):

    """
    Generate a HTML report from summary statistics and a given sample
    :param sample: DataFrame containing the sample you want to print
    :param stats_object: Dictionary containing summary statistics. Should be generated with an appropriate describe() function
    :return: String containing profile report in HTML format
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
            return str(value)

    def freq_table(freqtable, n, table_template, row_template, max_number_of_items_in_table):

        freq_rows_html = u''

        freq_other = sum(freqtable[max_number_of_items_in_table:])
        freq_missing = n - sum(freqtable)
        max_freq = max(freqtable.values[0], freq_other, freq_missing)
        try:
            min_freq = freqtable.values[max_number_of_items_in_table]
        except IndexError:
            min_freq = 0

        # TODO: Correctly sort missing and other

        def format_row(freq, label, extra_class=''):
            width = int(freq / max_freq * 99) + 1
            if width > 20:
                label_in_bar = freq
                label_after_bar = ""
            else:
                label_in_bar = "&nbsp;"
                label_after_bar = freq

            return row_template.format(label=label,
                                       width=width,
                                       count=freq,
                                       percentage='{:2.1f}'.format(freq / n * 100),
                                       extra_class=extra_class,
                                       label_in_bar=label_in_bar,
                                       label_after_bar=label_after_bar)

        for label, freq in six.iteritems(freqtable[0:max_number_of_items_in_table]):
            freq_rows_html += format_row(freq, label)

        if freq_other > min_freq:
            freq_rows_html += format_row(freq_other,
                                         "Other values (%s)" % (freqtable.count() - max_number_of_items_in_table),
                                         extra_class='other')

        if freq_missing > min_freq:
            freq_rows_html += format_row(freq_missing, "(Missing)", extra_class='missing')

        return table_template.format(rows=freq_rows_html, varid=hash(idx))

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
                                                           templates.mini_freq_table, templates.mini_freq_table_row, 3)
            formatted_values['freqtable'] = freq_table(stats_object['freq'][idx], n_obs,
                                                       templates.freq_table, templates.freq_table_row, 20)
            if row['distinct_count'] > 50:
                messages.append(templates.messages['HIGH_CARDINALITY'].format(formatted_values, varname = formatters.fmt_varname(idx)))
                row_classes['distinct_count'] = "alert"
            else:
                row_classes['distinct_count'] = ""

        if row['type'] == 'UNIQUE':
            obs = stats_object['freq'][idx].index

            formatted_values['firstn'] = pd.DataFrame(obs[0:3], columns=["First 3 values"]).to_html(classes="example_values", index=False)
            formatted_values['lastn'] = pd.DataFrame(obs[-3:], columns=["Last 3 values"]).to_html(classes="example_values", index=False)

            if n_obs > 40:
                formatted_values['firstn_expanded'] = pd.DataFrame(obs[0:20], index=range(1, 21)).to_html(classes="sample table table-hover", header=False)
                formatted_values['lastn_expanded'] = pd.DataFrame(obs[-20:], index=range(n_obs - 20 + 1, n_obs+1)).to_html(classes="sample table table-hover", header=False)
            else:
                formatted_values['firstn_expanded'] = pd.DataFrame(obs, index=range(1, n_obs+1)).to_html(classes="sample table table-hover", header=False)
                formatted_values['lastn_expanded'] = ''

        rows_html += templates.row_templates_dict[row['type']].format(formatted_values, row_classes=row_classes)

        if row['type'] in {'CORR', 'CONST'}:
            formatted_values['varname'] = formatters.fmt_varname(idx)
            messages.append(templates.messages[row['type']].format(formatted_values))


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

    overview_html = templates.overview_template.format(formatted_values, row_classes = row_classes, messages=messages_html)

    # Sample

    sample_html = templates.sample_html.format(sample_table_html=sample.to_html(classes="sample"))

    return templates.base_html % {'overview_html': overview_html, 'rows_html': rows_html, 'sample_html': sample_html}
