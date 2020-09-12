"""Plot functions for the profiling report."""
import copy
from typing import Optional, Union

import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import Patch
from matplotlib.ticker import FuncFormatter

from pandas_profiling.config import config
from pandas_profiling.utils.common import convert_timestamp_to_datetime
from pandas_profiling.visualisation.context import manage_matplotlib_context
from pandas_profiling.visualisation.utils import plot_360_n0sc0pe


def _plot_histogram(
    series: np.ndarray,
    bins: Union[int, np.ndarray],
    figsize: tuple = (6, 4),
    date=False,
):
    """Plot an histogram from the data and return the AxesSubplot object.

    Args:
        series: The data to plot
        figsize: The size of the figure (width, height) in inches, default (6,4)
        bins: number of bins (int for equal size, ndarray for variable size)

    Returns:
        The histogram plot.
    """
    fig = plt.figure(figsize=figsize)
    plot = fig.add_subplot(111)
    plot.set_ylabel("Frequency")

    # we have precomputed the histograms...
    diff = np.diff(bins)
    plot.bar(
        bins[:-1] + diff / 2,  # type: ignore
        series,
        diff,
        facecolor=config["html"]["style"]["primary_color"].get(str),
    )

    if date:

        def format_fn(tick_val, tick_pos):
            return convert_timestamp_to_datetime(tick_val).strftime("%Y-%m-%d %H:%M:%S")

        plot.xaxis.set_major_formatter(FuncFormatter(format_fn))

    if not config["plot"]["histogram"]["x_axis_labels"].get(bool):
        plot.set_xticklabels([])

    return plot


@manage_matplotlib_context()
def histogram(series: np.ndarray, bins: Union[int, np.ndarray], date=False) -> str:
    """Plot an histogram of the data.

    Args:
      series: The data to plot.
      bins: number of bins (int for equal size, ndarray for variable size)

    Returns:
      The resulting histogram encoded as a string.

    """
    plot = _plot_histogram(series, bins, date=date)
    plot.xaxis.set_tick_params(rotation=90 if date else 45)
    plot.figure.tight_layout()
    return plot_360_n0sc0pe(plt)


@manage_matplotlib_context()
def mini_histogram(series: np.ndarray, bins: Union[int, np.ndarray], date=False) -> str:
    """Plot a small (mini) histogram of the data.

    Args:
      series: The data to plot.
      bins: number of bins (int for equal size, ndarray for variable size)

    Returns:
      The resulting mini histogram encoded as a string.
    """
    plot = _plot_histogram(series, bins, figsize=(3, 2.25), date=date)
    plot.axes.get_yaxis().set_visible(False)
    plot.set_facecolor("w")

    for tick in plot.xaxis.get_major_ticks():
        tick.label1.set_fontsize(6 if date else 8)
    plot.xaxis.set_tick_params(rotation=90 if date else 45)
    plot.figure.tight_layout()

    return plot_360_n0sc0pe(plt)


def get_cmap_half(cmap):
    """Get the upper half of the color map

    Args:
        cmap: the color map

    Returns:
        A new color map based on the upper half of another color map

    References:
        https://stackoverflow.com/a/24746399/470433
    """
    # Evaluate an existing colormap from 0.5 (midpoint) to 1 (upper end)
    colors = cmap(np.linspace(0.5, 1, cmap.N // 2))

    # Create a new colormap from those colors
    return LinearSegmentedColormap.from_list("cmap_half", colors)


def get_correlation_font_size(n_labels) -> Optional[int]:
    """Dynamic label font sizes in correlation plots

    Args:
        n_labels: the number of labels

    Returns:
        A font size or None for the default font size
    """
    if n_labels > 100:
        font_size = 4
    elif n_labels > 80:
        font_size = 5
    elif n_labels > 50:
        font_size = 6
    elif n_labels > 40:
        font_size = 8
    else:
        return None
    return font_size


@manage_matplotlib_context()
def correlation_matrix(data: pd.DataFrame, vmin: int = -1) -> str:
    """Plot image of a matrix correlation.

    Args:
      data: The matrix correlation to plot.
      vmin: Minimum value of value range.

    Returns:
      The resulting correlation matrix encoded as a string.
    """
    fig_cor, axes_cor = plt.subplots()
    cmap_name = config["plot"]["correlation"]["cmap"].get(str)
    cmap_bad = config["plot"]["correlation"]["bad"].get(str)

    cmap = plt.get_cmap(cmap_name)
    if vmin == 0:
        cmap = get_cmap_half(cmap)
    cmap = copy.copy(cmap)
    cmap.set_bad(cmap_bad)

    labels = data.columns
    matrix_image = axes_cor.imshow(
        data, vmin=vmin, vmax=1, interpolation="nearest", cmap=cmap
    )
    plt.colorbar(matrix_image)

    if data.isnull().values.any():
        legend_elements = [Patch(facecolor=cmap(np.nan), label="invalid\ncoefficient")]

        plt.legend(
            handles=legend_elements,
            loc="upper right",
            handleheight=2.5,
        )

    axes_cor.set_xticks(np.arange(0, data.shape[0], float(data.shape[0]) / len(labels)))
    axes_cor.set_yticks(np.arange(0, data.shape[1], float(data.shape[1]) / len(labels)))

    font_size = get_correlation_font_size(len(labels))
    axes_cor.set_xticklabels(labels, rotation=90, fontsize=font_size)
    axes_cor.set_yticklabels(labels, fontsize=font_size)
    plt.subplots_adjust(bottom=0.2)

    return plot_360_n0sc0pe(plt)


@manage_matplotlib_context()
def scatter_complex(series: pd.Series) -> str:
    """Scatter plot (or hexbin plot) from a series of complex values

    Examples:
        >>> complex_series = pd.Series([complex(1, 3), complex(3, 1)])
        >>> scatter_complex(complex_series)

    Args:
        series: the Series

    Returns:
        A string containing (a reference to) the image
    """
    plt.ylabel("Imaginary")
    plt.xlabel("Real")

    color = config["html"]["style"]["primary_color"].get(str)
    scatter_threshold = config["plot"]["scatter_threshold"].get(int)

    if len(series) > scatter_threshold:
        cmap = sns.light_palette(color, as_cmap=True)
        plt.hexbin(series.real, series.imag, cmap=cmap)
    else:
        plt.scatter(series.real, series.imag, color=color)

    return plot_360_n0sc0pe(plt)


@manage_matplotlib_context()
def scatter_series(series, x_label="Width", y_label="Height") -> str:
    """Scatter plot (or hexbin plot) from one series of sequences with length 2

    Examples:
        >>> scatter_series(file_sizes, "Width", "Height")

    Args:
        series: the Series
        x_label: the label on the x-axis
        y_label: the label on the y-axis

    Returns:
        A string containing (a reference to) the image
    """
    plt.xlabel(x_label)
    plt.ylabel(y_label)

    color = config["html"]["style"]["primary_color"].get(str)
    scatter_threshold = config["plot"]["scatter_threshold"].get(int)

    if len(series) > scatter_threshold:
        cmap = sns.light_palette(color, as_cmap=True)
        plt.hexbin(*zip(*series.tolist()), cmap=cmap)
    else:
        plt.scatter(*zip(*series.tolist()), color=color)
    return plot_360_n0sc0pe(plt)


@manage_matplotlib_context()
def scatter_pairwise(series1, series2, x_label, y_label) -> str:
    """Scatter plot (or hexbin plot) from two series

    Examples:
        >>> widths = pd.Series([800, 1024])
        >>> heights = pd.Series([600, 768])
        >>> scatter_series(widths, heights, "Width", "Height")

    Args:
        series1: the series corresponding to the x-axis
        series2: the series corresponding to the y-axis
        x_label: the label on the x-axis
        y_label: the label on the y-axis

    Returns:
        A string containing (a reference to) the image
    """
    plt.xlabel(x_label)
    plt.ylabel(y_label)

    color = config["html"]["style"]["primary_color"].get(str)
    scatter_threshold = config["plot"]["scatter_threshold"].get(int)

    indices = (series1.notna()) & (series2.notna())

    if len(series1) > scatter_threshold:
        cmap = sns.light_palette(color, as_cmap=True)
        plt.hexbin(series1[indices], series2[indices], gridsize=15, cmap=cmap)
    else:
        plt.scatter(series1[indices], series2[indices], color=color)
    return plot_360_n0sc0pe(plt)


@manage_matplotlib_context()
def pie_plot(data, legend_kws=None):
    if legend_kws is None:
        legend_kws = {}

    def func(pct, allvals):
        absolute = int(pct / 100.0 * np.sum(allvals))
        return "{:.1f}%\n({:d})".format(pct, absolute)

    wedges, _, _ = plt.pie(
        data, autopct=lambda pct: func(pct, data), textprops=dict(color="w")
    )
    plt.legend(wedges, data.index.values, **legend_kws)

    return plot_360_n0sc0pe(plt)
