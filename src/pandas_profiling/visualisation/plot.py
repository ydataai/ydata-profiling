"""Plot functions for the profiling report."""

from typing import Union

import matplotlib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from pandas.plotting import register_matplotlib_converters
from pandas_profiling.visualisation.utils import plot_360_n0sc0pe
from pkg_resources import resource_filename

from pandas_profiling.config import config
from pandas_profiling.model.base import Variable

register_matplotlib_converters()
matplotlib.style.use(resource_filename(__name__, "pandas_profiling.mplstyle"))
sns.set_style(style="white")


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
            facecolor=config["html"]["style"]["primary_color"].get(str),
            bins=bins,
        )

    else:
        plot = series.plot(
            kind="hist",
            figsize=figsize,
            facecolor=config["html"]["style"]["primary_color"].get(str),
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


def scatter_complex(series) -> str:
    plt.ylabel("Imaginary")
    plt.xlabel("Real")

    if len(series) > 1000:
        plt.hexbin(series.real, series.imag)
    else:
        plt.scatter(series.real, series.imag)

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

    if len(series) > 1000:
        plt.hexbin(*zip(*series.tolist()))
    else:
        plt.scatter(*zip(*series.tolist()))
    return plot_360_n0sc0pe(plt)


def scatter_pairwise(series1, series2, x_label, y_label) -> str:
    plt.xlabel(x_label)
    plt.ylabel(y_label)

    if len(series1) > 1000:
        color = config["html"]["style"]["primary_color"].get(str)
        cmap = sns.light_palette(color, as_cmap=True)
        plt.hexbin(series1.tolist(), series2.tolist(), gridsize=15, cmap=cmap)
    else:
        plt.scatter(series1.tolist(), series2.tolist())
    return plot_360_n0sc0pe(plt)
