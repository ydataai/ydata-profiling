"""Plot functions for the profiling report."""

import base64
from io import BytesIO
from urllib.parse import quote

import matplotlib
import missingno
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from pandas.plotting import register_matplotlib_converters
from pkg_resources import resource_filename

from pandas_profiling import config
from pandas_profiling.model.base import Variable
from pandas_profiling.view.formatters import hex_to_rgb

register_matplotlib_converters()
matplotlib.style.use(resource_filename(__name__, "pandas_profiling.mplstyle"))


def _plot_histogram(
    series: pd.Series, series_description: dict, figsize: tuple = (6, 4)
):
    """Plot an histogram from the data and return the AxesSubplot object.

    Args:
        series: The data to plot
        figsize: The size of the figure (width, height) in inches, default (6,4)

    Returns:
        The histogram plot.
    """

    # Bins should never be larger than the number of distinct values
    bins = config["plot"]["histogram"]["bins"].get(int)
    bins = min(series_description["distinct_count_with_nan"], bins)

    if series_description["type"] == Variable.TYPE_DATE:
        # Workaround for https://github.com/pandas-dev/pandas/issues/17372
        fig = plt.figure(figsize=figsize)
        plot = fig.add_subplot(111)
        plot.set_ylabel("Frequency")
        plot.hist(
            series.dropna().values,
            facecolor=config["plot"]["face_color"].get(str),
            bins=bins,
        )

    else:
        plot = series.plot(
            kind="hist",
            figsize=figsize,
            facecolor=config["plot"]["face_color"].get(str),
            bins=bins,
        )
    return plot


def histogram(series: pd.Series, series_description: dict) -> str:
    """Plot an histogram of the data.

    Args:
      series_description:
      series: The data to plot.

    Returns:
      The resulting histogram encoded as a string.

    """
    plot = _plot_histogram(series, series_description)
    plot.xaxis.set_tick_params(rotation=45)
    plot.figure.tight_layout()

    return plot_360_n0sc0pe(plt)


def mini_histogram(series: pd.Series, series_description: dict) -> str:
    """Plot a small (mini) histogram of the data.

    Args:
      series_description:
      series: The data to plot.

    Returns:
      The resulting mini histogram encoded as a string.
    """
    plot = _plot_histogram(series, series_description, figsize=(2, 1.5))
    plot.axes.get_yaxis().set_visible(False)
    plot.set_facecolor("w")

    xticks = plot.xaxis.get_major_ticks()
    for tick in xticks:
        tick.label1.set_fontsize(8)
    plot.xaxis.set_tick_params(rotation=45)
    plot.figure.tight_layout()

    return plot_360_n0sc0pe(plt)


def correlation_matrix(data: pd.DataFrame, vmin: int = -1) -> str:
    """Plot image of a matrix correlation.

    Args:
      data: The matrix correlation to plot.
      vmin: Minimum value of value range.

    Returns:
      The resulting correlation matrix encoded as a string.
    """
    fig_cor, axes_cor = plt.subplots(1, 1)
    labels = data.columns
    matrix_image = axes_cor.imshow(
        data,
        vmin=vmin,
        vmax=1,
        interpolation="nearest",
        cmap=config["plot"]["correlation"]["cmap"].get(str),
    )
    plt.colorbar(matrix_image)
    axes_cor.set_xticks(np.arange(0, data.shape[0], float(data.shape[0]) / len(labels)))
    axes_cor.set_yticks(np.arange(0, data.shape[1], float(data.shape[1]) / len(labels)))
    axes_cor.set_xticklabels(labels, rotation=90)
    axes_cor.set_yticklabels(labels)
    plt.subplots_adjust(bottom=0.2)

    return plot_360_n0sc0pe(plt)


def missing_matrix(data: pd.DataFrame) -> str:
    """Generate missing values matrix plot

    Args:
      data: Pandas DataFrame to generate missing values matrix from.

    Returns:
      The resulting missing values matrix encoded as a string.
    """
    missingno.matrix(
        data,
        figsize=(10, 4),
        color=hex_to_rgb(config["plot"]["face_color"].get(str)),
        fontsize=14,
        sparkline=False,
    )
    plt.subplots_adjust(left=0.1, right=0.9, top=0.7, bottom=0.2)
    return plot_360_n0sc0pe(plt)


def missing_bar(data: pd.DataFrame) -> str:
    """Generate missing values bar plot.

    Args:
      data: Pandas DataFrame to generate missing values bar plot from.

    Returns:
      The resulting missing values bar plot encoded as a string.
    """
    missingno.bar(
        data,
        figsize=(10, 4),
        color=hex_to_rgb(config["plot"]["face_color"].get(str)),
        fontsize=14,
    )
    for ax0 in plt.gcf().get_axes():
        ax0.grid(False)
    plt.subplots_adjust(left=0.1, right=0.9, top=0.8, bottom=0.3)
    return plot_360_n0sc0pe(plt)


def missing_heatmap(data: pd.DataFrame) -> str:
    """Generate missing values heatmap plot.

    Args:
      data: Pandas DataFrame to generate missing values heatmap plot from.

    Returns:
      The resulting missing values heatmap plot encoded as a string.
    """
    missingno.heatmap(
        data,
        figsize=(10, 4),
        fontsize=14,
        cmap=config["plot"]["missing"]["cmap"].get(str),
    )
    plt.subplots_adjust(left=0.2, right=0.9, top=0.8, bottom=0.3)
    return plot_360_n0sc0pe(plt)


def missing_dendrogram(data: pd.DataFrame) -> str:
    """Generate a dendrogram plot for missing values.

    Args:
      data: Pandas DataFrame to generate missing values dendrogram plot from.

    Returns:
      The resulting missing values dendrogram plot encoded as a string.

    """
    missingno.dendrogram(data, figsize=(10, 4), fontsize=14)
    plt.subplots_adjust(left=0.1, right=0.9, top=0.7, bottom=0.2)
    return plot_360_n0sc0pe(plt)


def plot_360_n0sc0pe(plt) -> str:
    """Quickscope the plot to a base64 encoded string.

    Args:
        plt: The pyplot module.
        img_format: The format in which to store the image: 'svg' or 'png'. (Default value = 'svg')

    Returns:
        A base64 encoded version of the plot in the specified image format.
    """
    img_format = config["plot"]["image_format"].get(str)
    if img_format not in ["svg", "png"]:
        raise ValueError('Can only 360 n0sc0pe "png" or "svg" format')

    mime_types = {"png": "image/png", "svg": "image/svg+xml"}

    try:
        image_data = BytesIO()
        plt.savefig(image_data, format=img_format)
        image_data.seek(0)
        result_string = "data:{mime_type};base64,{image_data}".format(
            mime_type=mime_types[img_format],
            image_data=quote(base64.b64encode(image_data.getvalue())),
        )
        plt.close()
    except RuntimeError:
        # Hack https://stackoverflow.com/questions/44666207/matplotlib-error-when-running-plotting-in-multiprocess
        # #comment79373127_44666207
        return plot_360_n0sc0pe(plt)
    return result_string
