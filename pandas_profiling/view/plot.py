"""Plot functions for the profiling report."""

import base64
from io import BytesIO
from typing import Union
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
    series: pd.Series,
    series_description: dict,
    bins: Union[int, np.ndarray],
    figsize: tuple = (6, 4),
):
    """Plot an histogram from the data and return the AxesSubplot object.

    Args:
        series: The data to plot
        figsize: The size of the figure (width, height) in inches, default (6,4)
        bins: number of bins (int for equal size, ndarray for variable size)

    Returns:
        The histogram plot.


    """
    if series_description["type"] == Variable.TYPE_DATE:
        # Workaround for https://github.com/pandas-dev/pandas/issues/17372
        fig = plt.figure(figsize=figsize)
        plot = fig.add_subplot(111)
        plot.set_ylabel("Frequency")
        plot.hist(
            series.dropna().values,
            facecolor=config["style"]["primary_color"].get(str),
            bins=bins,
        )

    else:
        plot = series.plot(
            kind="hist",
            figsize=figsize,
            facecolor=config["style"]["primary_color"].get(str),
            bins=bins,
        )
    return plot


def histogram(
    series: pd.Series, series_description: dict, bins: Union[int, np.ndarray]
) -> str:
    """Plot an histogram of the data.

    Args:
      series_description:
      series: The data to plot.
      bins: number of bins (int for equal size, ndarray for variable size)

    Returns:
      The resulting histogram encoded as a string.

    """
    plot = _plot_histogram(series, series_description, bins)
    plot.xaxis.set_tick_params(rotation=45)
    plot.figure.tight_layout()

    return plot_360_n0sc0pe(plt)


def mini_histogram(
    series: pd.Series, series_description: dict, bins: Union[int, np.ndarray]
) -> str:
    """Plot a small (mini) histogram of the data.

    Args:
      series_description:
      series: The data to plot.
      bins: number of bins (int for equal size, ndarray for variable size)

    Returns:
      The resulting mini histogram encoded as a string.
    """
    plot = _plot_histogram(series, series_description, bins, figsize=(2, 1.5))
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


def get_font_size(data):
    """Calculate font size based on number of columns

    Args:
        data: DataFrame

    Returns:
        Font size for missing values plots.
    """
    max_label_length = max([len(label) for label in data.columns])

    if len(data.columns) < 20:
        font_size = 13
    elif 20 <= len(data.columns) < 40:
        font_size = 12
    elif 40 <= len(data.columns) < 60:
        font_size = 10
    else:
        font_size = 8

    font_size *= min(1.0, 20.0 / max_label_length)
    return font_size


def missing_matrix(data: pd.DataFrame) -> str:
    """Generate missing values matrix plot

    Args:
      data: Pandas DataFrame to generate missing values matrix from.

    Returns:
      The resulting missing values matrix encoded as a string.
    """
    labels = config["plot"]["missing"]["force_labels"].get(bool)
    missingno.matrix(
        data,
        figsize=(10, 4),
        color=hex_to_rgb(config["style"]["primary_color"].get(str)),
        fontsize=get_font_size(data) / 20 * 16,
        sparkline=False,
        labels=labels,
    )
    plt.subplots_adjust(left=0.1, right=0.9, top=0.7, bottom=0.2)
    # Note: override image format, svg contains bug for missingno.matrix
    return plot_360_n0sc0pe(plt, image_format="png")


def missing_bar(data: pd.DataFrame) -> str:
    """Generate missing values bar plot.

    Args:
      data: Pandas DataFrame to generate missing values bar plot from.

    Returns:
      The resulting missing values bar plot encoded as a string.
    """
    labels = config["plot"]["missing"]["force_labels"].get(bool)
    missingno.bar(
        data,
        figsize=(10, 5),
        color=hex_to_rgb(config["style"]["primary_color"].get(str)),
        fontsize=get_font_size(data),
        labels=labels,
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

    height = 4
    if len(data.columns) > 10:
        height += int((len(data.columns) - 10) / 5)
    height = min(height, 10)

    font_size = get_font_size(data)
    if len(data.columns) > 40:
        font_size /= 1.4

    labels = config["plot"]["missing"]["force_labels"].get(bool)
    missingno.heatmap(
        data,
        figsize=(10, height),
        fontsize=font_size,
        cmap=config["plot"]["missing"]["cmap"].get(str),
        labels=labels,
    )

    if len(data.columns) > 40:
        plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.3)
    else:
        plt.subplots_adjust(left=0.2, right=0.9, top=0.8, bottom=0.3)

    return plot_360_n0sc0pe(plt)


def missing_dendrogram(data: pd.DataFrame) -> str:
    """Generate a dendrogram plot for missing values.

    Args:
      data: Pandas DataFrame to generate missing values dendrogram plot from.

    Returns:
      The resulting missing values dendrogram plot encoded as a string.

    """
    missingno.dendrogram(data, fontsize=get_font_size(data) * 2.0)
    plt.subplots_adjust(left=0.1, right=0.9, top=0.7, bottom=0.2)
    return plot_360_n0sc0pe(plt)


def plot_360_n0sc0pe(plt, image_format=None, attempts=0) -> str:
    """Quickscope the plot to a base64 encoded string.

    Args:
        image_format: png or svg, overrides config.
        plt: The pyplot module.
        attempts: number to tries

    Returns:
        A base64 encoded version of the plot in the specified image format.
    """
    if image_format is None:
        image_format = config["plot"]["image_format"].get(str)
    dpi = config["plot"]["dpi"].get(int)

    if image_format not in ["svg", "png"]:
        raise ValueError('Can only 360 n0sc0pe "png" or "svg" format.')

    mime_types = {"png": "image/png", "svg": "image/svg+xml"}

    try:
        image_data = BytesIO()
        plt.savefig(image_data, dpi=dpi, format=image_format)
        image_data.seek(0)
        result_string = "data:{mime_type};base64,{image_data}".format(
            mime_type=mime_types[image_format],
            image_data=quote(base64.b64encode(image_data.getvalue())),
        )
        plt.close()
    except RuntimeError:
        plt.close()
        # Hack https://stackoverflow.com/questions/44666207/matplotlib-error-when-running-plotting-in-multiprocess
        # #comment79373127_44666207
        if attempts > 10:
            return ""
        else:
            return plot_360_n0sc0pe(plt, attempts + 1)
    return result_string
