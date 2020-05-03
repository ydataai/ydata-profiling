"""Plot functions for the profiling report."""

from typing import Optional, Union

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import Patch
from pandas.plotting import register_matplotlib_converters
from pkg_resources import resource_filename

from pandas_profiling.config import config
from pandas_profiling.visualisation.utils import plot_360_n0sc0pe

register_matplotlib_converters()
matplotlib.style.use(resource_filename(__name__, "pandas_profiling.mplstyle"))
sns.set_style(style="white")


def _plot_histogram(
    series: np.ndarray,
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
    # if series_description["type"] == Variable.TYPE_DATE:
    # Workaround for https://github.com/pandas-dev/pandas/issues/17372
    fig = plt.figure(figsize=figsize)
    plot = fig.add_subplot(111)
    plot.set_ylabel("Frequency")
    plot.hist(
        series,  # .dropna().values,
        facecolor=config["html"]["style"]["primary_color"].get(str),
        bins=bins,
    )
    # else:
    #     plot = series.plot(
    #         kind="hist",
    #         figsize=figsize,
    #         facecolor=config["html"]["style"]["primary_color"].get(str),
    #         bins=bins,
    #     )
    return plot


def histogram(
    series: np.ndarray, series_description: dict, bins: Union[int, np.ndarray]
) -> str:
    """Plot an histogram of the data.

    Args:
      series: The data to plot.
      series_description:
      bins: number of bins (int for equal size, ndarray for variable size)

    Returns:
      The resulting histogram encoded as a string.

    """
    plot = _plot_histogram(series, series_description, bins)
    plot.xaxis.set_tick_params(rotation=45)
    plot.figure.tight_layout()

    return plot_360_n0sc0pe(plt)


def mini_histogram(
    series: np.ndarray, series_description: dict, bins: Union[int, np.ndarray]
) -> str:
    """Plot a small (mini) histogram of the data.

    Args:
      series: The data to plot.
      series_description:
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
    cmap.set_bad(cmap_bad)

    labels = data.columns
    matrix_image = axes_cor.imshow(
        data, vmin=vmin, vmax=1, interpolation="nearest", cmap=cmap
    )
    plt.colorbar(matrix_image)

    if data.isnull().values.any():
        legend_elements = [Patch(facecolor=cmap(np.nan), label="invalid\ncoefficient")]

        plt.legend(
            handles=legend_elements, loc="upper right", handleheight=2.5,
        )

    axes_cor.set_xticks(np.arange(0, data.shape[0], float(data.shape[0]) / len(labels)))
    axes_cor.set_yticks(np.arange(0, data.shape[1], float(data.shape[1]) / len(labels)))

    font_size = get_correlation_font_size(len(labels))
    axes_cor.set_xticklabels(labels, rotation=90, fontsize=font_size)
    axes_cor.set_yticklabels(labels, fontsize=font_size)
    plt.subplots_adjust(bottom=0.2)

    return plot_360_n0sc0pe(plt)


def scatter_complex(series) -> str:
    plt.ylabel("Imaginary")
    plt.xlabel("Real")

    color = config["html"]["style"]["primary_color"].get(str)

    if len(series) > 1000:
        cmap = sns.light_palette(color, as_cmap=True)
        plt.hexbin(series.real, series.imag, cmap=cmap)
    else:
        plt.scatter(series.real, series.imag, color=color)

    return plot_360_n0sc0pe(plt)


def scatter_series(series, x_label="Width", y_label="Height") -> str:
    """

    Examples:
        >>> scatter_series(file_sizes, "Width", "Height")

    Args:
        series:
        x_label:
        y_label:

    Returns:

    """
    plt.xlabel(x_label)
    plt.ylabel(y_label)

    color = config["html"]["style"]["primary_color"].get(str)

    if len(series) > 1000:
        cmap = sns.light_palette(color, as_cmap=True)
        plt.hexbin(*zip(*series.tolist()), cmap=cmap)
    else:
        plt.scatter(*zip(*series.tolist()), color=color)
    return plot_360_n0sc0pe(plt)


def scatter_pairwise(series1, series2, x_label, y_label) -> str:
    plt.xlabel(x_label)
    plt.ylabel(y_label)

    color = config["html"]["style"]["primary_color"].get(str)

    if len(series1) > 1000:
        cmap = sns.light_palette(color, as_cmap=True)
        plt.hexbin(series1.tolist(), series2.tolist(), gridsize=15, cmap=cmap)
    else:
        plt.scatter(series1.tolist(), series2.tolist(), color=color)
    return plot_360_n0sc0pe(plt)
