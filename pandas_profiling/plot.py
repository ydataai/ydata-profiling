# -*- coding: utf-8 -*-
"""Plot distribution of datasets"""

import base64
from distutils.version import LooseVersion
import pandas_profiling.base as base
import matplotlib
import numpy as np
# Fix #68, this call is not needed and brings side effects in some use cases
# Backend name specifications are not case-sensitive; e.g., ‘GTKAgg’ and ‘gtkagg’ are equivalent.
# See https://matplotlib.org/faq/usage_faq.html#what-is-a-backend
BACKEND = 'Agg'
if matplotlib.get_backend().lower() != BACKEND.lower():
    # If backend is not set properly a call to describe will hang
    matplotlib.use(BACKEND)
from matplotlib import pyplot as plt
try:
    from StringIO import BytesIO
except ImportError:
    from io import BytesIO
try:
    from urllib import quote
except ImportError:
    from urllib.parse import quote

def _plot_histogram(series, bins=10, figsize=(6, 4), facecolor='#337ab7'):
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
    try:
        plot = series.hist(figsize=figsize,
                           facecolor=facecolor,
                           bins=bins)  # TODO when running on server, send this off to a different thread
    except TypeError:  # matplotlib 1.4 can't plot dates so will show empty plot instead
        pass
    return plot


def histogram(series, bins=10, **kwargs):
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
    plot = _plot_histogram(series, bins=bins)
    plot.xaxis.set_tick_params(rotation=45)
    plot.figure.tight_layout()
    plot.figure.savefig(imgdata)
    imgdata.seek(0)
    result_string = 'data:image/png;base64,' + quote(base64.b64encode(imgdata.getvalue()))
    # TODO Think about writing this to disk instead of caching them in strings
    plt.close(plot.figure)
    return result_string


def mini_histogram(series, bins=10, **kwargs):
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
    plot = _plot_histogram(series, bins=bins, figsize=(2, 1.5), **kwargs)
    plot.axes.get_yaxis().set_visible(False)

    if LooseVersion(matplotlib.__version__) <= '1.5.9':
        plot.set_axis_bgcolor("w")
    else:
        plot.set_facecolor("w")

    xticks = plot.xaxis.get_major_ticks()
    for tick in xticks:
        tick.label.set_fontsize(8)
    plot.xaxis.set_tick_params(rotation=45)
    plot.figure.tight_layout()
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
    axes_cor.set_xticklabels(labels, rotation=45)
    axes_cor.set_yticklabels(labels)

    matrix_image.figure.savefig(imgdata, bbox_inches='tight')
    imgdata.seek(0)
    result_string = 'data:image/png;base64,' + quote(base64.b64encode(imgdata.getvalue()))
    plt.close(matrix_image.figure)
    return result_string