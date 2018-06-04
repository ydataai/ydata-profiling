# -*- coding: utf-8 -*-
"""Plot distribution of datasets"""

import base64
from distutils.version import LooseVersion
import pandas_profiling.base as base
from matplotlib import pyplot as plt
import matplotlib
import numpy as np
# Fix #68, this call is not needed and brings side effects in some use cases
# Backend name specifications are not case-sensitive; e.g., ‘GTKAgg’ and ‘gtkagg’ are equivalent.
# See https://matplotlib.org/faq/usage_faq.html#what-is-a-backend
BACKEND = matplotlib.get_backend()
if matplotlib.get_backend().lower() != BACKEND.lower():
    # If backend is not set properly a call to describe will hang
    matplotlib.use(BACKEND)

try:
    from StringIO import BytesIO
except ImportError:
    from io import BytesIO
try:
    from urllib import quote
except ImportError:
    from urllib.parse import quote

def _plot_histogram(series, bins=10, figsize=(6, 4), facecolor='#337ab7', **kwargs):
    """Plot an histogram from the data and return the AxesSubplot object.

    Parameters
    ----------
    series : Series
        The data to plot
    figsize : tuple
        The size of the figure (width, height) in inches, default (6,4)
    facecolor : str
        The color code.

    Returns
    -------
    matplotlib.AxesSubplot
        The plot.
    """

    if "target_series" in kwargs.keys():
        target_series = kwargs["target_series"]
        is_target = True
    else :
        is_target = False
        target_series = None

    if base.get_vartype(series) == base.TYPE_DATE:
        # TODO: These calls should be merged
        fig = plt.figure(figsize=figsize)
        plot = fig.add_subplot(111)
        plot.set_ylabel('Frequency')
        try:
            plot.hist(series.dropna().values, facecolor=facecolor, bins=bins)
        except TypeError: # matplotlib 1.4 can't plot dates so will show empty plot instead
            pass
        return plot
    else:

        if is_target:
            non_null_series = series[~series.isnull()]
            bins_limit = np.histogram(non_null_series, bins)[1]
            
            fig, ax1 = plt.subplots(figsize=figsize)
            ax1.set_ylabel('Frequency', color=facecolor)
            avg_target = []
            avg_bins = []

            for min_, max_ in [(bins_limit[i], bins_limit[i+1]) for i in xrange(len(bins_limit)-1)]:
                mask = (series >= min_) & (series <= max_) # create bin mask
                avg_target.append(target_series[mask].mean()) # get mean of elements in bin
                avg_bins.append(float(min_+max_) / 2) # center of the bin
            ax1.hist(non_null_series, bins=bins)

            ax2 = ax1.twinx()
            ax2.plot(avg_bins, avg_target, '-o', color='#fcab10')
            ax2.set_ylabel('Averaged_%s'%(kwargs['target_name']), color='#fcab10')
            ax2.grid(False)
            return fig.get_axes()[1]
        else:
            plot = series.plot(kind='hist', figsize=figsize,
                           facecolor=facecolor,
                           bins=bins)  # TODO when running on server, send this off to a different thread
            return plot



def histogram(series, **kwargs):
    """Plot an histogram of the data.

    Parameters
    ----------
    series: Series
        The data to plot.

    Returns
    -------
    str
        The resulting image encoded as a string.
    """
    imgdata = BytesIO()
    plot = _plot_histogram(series, **kwargs)
    if 'target_name' in kwargs.keys():
        plot.figure.subplots_adjust(left=0.15, right=0.85, top=0.9, bottom=0.1, wspace=0, hspace=0)
    else :
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
    series: Series
        The data to plot.

    Returns
    -------
    str
        The resulting image encoded as a string.
    """
    imgdata = BytesIO()
    plot = _plot_histogram(series, figsize=(2, 0.75), **kwargs)
    if 'target_name' in kwargs.keys():
        for ax in plot.figure.get_axes():
            ax.grid(False)
            ax.get_yaxis().set_visible(False)
            ax.get_xaxis().set_visible(False)
            ax.facecolor = 'white'

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

def correlation_matrix(corrdf, title, **kwargs):
    """Plot image of a matrix correlation.
    Parameters
    ----------
    corrdf: DataFrame
        The matrix correlation to plot.
    title: str
        The matrix title
    Returns
    -------
    str, The resulting image encoded as a string.
    """
    imgdata = BytesIO()
    fig_cor, axes_cor = plt.subplots(1, 1)
    labels = corrdf.columns
    matrix_image = axes_cor.imshow(corrdf, vmin=-1, vmax=1, interpolation="nearest", cmap='bwr')
    plt.title(title, size=18)
    plt.colorbar(matrix_image)
    axes_cor.set_xticks(np.arange(0, corrdf.shape[0], corrdf.shape[0] * 1.0 / len(labels)))
    axes_cor.set_yticks(np.arange(0, corrdf.shape[1], corrdf.shape[1] * 1.0 / len(labels)))
    axes_cor.set_xticklabels(labels, rotation=90)
    axes_cor.set_yticklabels(labels)

    matrix_image.figure.savefig(imgdata, bbox_inches='tight')
    imgdata.seek(0)
    result_string = 'data:image/png;base64,' + quote(base64.b64encode(imgdata.getvalue()))
    plt.close(matrix_image.figure)
    return result_string
