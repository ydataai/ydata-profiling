"""Plot functions for the profiling report."""
import contextlib
import copy
import warnings
from typing import Optional

import matplotlib
import matplotlib.cbook
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.figure import Figure
from matplotlib.patches import Patch
from matplotlib.ticker import FuncFormatter
from missingno import missingno
from pandas.plotting import (
    deregister_matplotlib_converters,
    register_matplotlib_converters,
)
from scipy import stats

from pandas_profiling.config import config
from pandas_profiling.report.presentation.core import Image
from pandas_profiling.utils.common import convert_timestamp_to_datetime
from pandas_profiling.visualisation.plot import PlotRegister, render_plot
from pandas_profiling.visualisation.utils import hex_to_rgb, plot_360_n0sc0pe


@render_plot.register(Figure)
def _(plot_obj: Figure, alt: str, name: str, anchor_id: str, *args, **kwargs):
    image_format = config["plot"]["image_format"].get(str)

    return Image(
        plot_360_n0sc0pe(plot_obj),
        image_format=image_format,
        alt=alt,
        name=name,
        anchor_id=anchor_id,
    )


def histogram_compute(finite_values, n_unique, name="histogram"):
    stats = {}
    bins = config["plot"]["histogram"]["bins"].get(int)
    bins = "auto" if bins == 0 else min(bins, n_unique)
    stats[name] = np.histogram(finite_values, bins)

    max_bins = config["plot"]["histogram"]["max_bins"].get(int)
    if bins == "auto" and len(stats[name][1]) > max_bins:
        stats[name] = np.histogram(finite_values, max_bins)

    return stats


@contextlib.contextmanager
def manage_matplotlib_context():
    """Return a context manager for temporarily changing matplotlib unit registries and rcParams."""
    originalRcParams = matplotlib.rcParams.copy()

    ## Credits for this style go to the ggplot and seaborn packages.
    ##   We copied the style file to remove dependencies on the Seaborn package.
    ##   Check it out, it's an awesome library for plotting
    customRcParams = {
        "patch.facecolor": "#348ABD",  # blue
        "patch.antialiased": True,
        "font.size": 10.0,
        "figure.edgecolor": "0.50",
        # Seaborn common parameters
        "figure.facecolor": "white",
        "text.color": ".15",
        "axes.labelcolor": ".15",
        # legend.frameon: False
        "legend.numpoints": 1,
        "legend.scatterpoints": 1,
        "xtick.direction": "out",
        "ytick.direction": "out",
        "xtick.color": ".15",
        "ytick.color": ".15",
        "axes.axisbelow": True,
        "image.cmap": "Greys",
        "font.family": ["sans-serif"],
        "font.sans-serif": [
            "Arial",
            "Liberation Sans",
            "Bitstream Vera Sans",
            "sans-serif",
        ],
        "grid.linestyle": "-",
        "lines.solid_capstyle": "round",
        # Seaborn darkgrid parameters
        # .15 = dark_gray
        # .8 = light_gray
        "axes.grid": True,
        "axes.facecolor": "#EAEAF2",
        "axes.edgecolor": "white",
        "axes.linewidth": 0,
        "grid.color": "white",
        # Seaborn notebook context
        "figure.figsize": [8.0, 5.5],
        "axes.labelsize": 11,
        "axes.titlesize": 12,
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
        "legend.fontsize": 10,
        "grid.linewidth": 1,
        "lines.linewidth": 1.75,
        "patch.linewidth": 0.3,
        "lines.markersize": 7,
        "lines.markeredgewidth": 0,
        "xtick.major.width": 1,
        "ytick.major.width": 1,
        "xtick.minor.width": 0.5,
        "ytick.minor.width": 0.5,
        "xtick.major.pad": 7,
        "ytick.major.pad": 7,
        "figure.autolayout": True,
    }

    try:
        register_matplotlib_converters()
        matplotlib.rcParams.update(customRcParams)
        sns.set_style(style="white")
        yield
    finally:
        deregister_matplotlib_converters()  # revert to original unit registries
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=matplotlib.cbook.mplDeprecation)
            matplotlib.rcParams.update(originalRcParams)  # revert to original rcParams


def _plot_histogram(
    series: pd.Series,
    figsize: tuple = (6, 4),
    date=False,
) -> Figure:
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

    series, bins = np.histogram(series.index, weights=series.values)
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

    return fig


@PlotRegister.register()
@manage_matplotlib_context()
def histogram(series: pd.Series):  # , bins: Union[int, np.ndarray], date=False) -> str:
    """Plot an histogram of the data.

    Args:
      series: The data to plot.
      bins: number of bins (int for equal size, ndarray for variable size)

    Returns:
      The resulting histogram encoded as a string.

    """
    date = False
    fig = _plot_histogram(series, date=date)
    # ax = fig.gca()
    # ax.set_tick_params(rotation=90 if date else 45)
    return fig


@PlotRegister.register()
@manage_matplotlib_context()
def bar(series: pd.Series):
    fig, ax = plt.subplots()
    ax.barh(series.index, series.values)
    ax.invert_yaxis()
    return fig


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


@PlotRegister.register()
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
    # plt.subplots_adjust(bottom=0.2)

    return fig_cor


@PlotRegister.register()
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

    return plt.gcf()


@PlotRegister.register()
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
    return plt.gcf()


@PlotRegister.register()
@manage_matplotlib_context()
def heatmap(data, x_label, y_label) -> str:
    fig = plt.figure()

    # TODO: configure n_max
    # TODO: configure cmap
    # TODO: use precomputed value counts

    # TODO: group other values
    n_max = 25
    cmap = "viridis"

    series1 = data[x_label]
    series2 = data[y_label]
    top1 = series1.value_counts()
    n_top1 = len(top1)
    if n_top1 > n_max:
        top1 = top1.head(n_max)
        x_label += f" (top-{n_max} of {n_top1})"

    top2 = series2.value_counts()
    n_top2 = len(top2)
    if n_top2 > n_max:
        top2 = top2.head(n_max)
        y_label += f" (top-{n_max} of {n_top2})"
    df = pd.crosstab(
        series2[series2.isin(top2.index)], series1[series1.isin(top1.index)]
    )

    heatmap = plt.pcolor(df, cmap=cmap)

    # Add text
    for y in range(df.shape[0]):
        for x in range(df.shape[1]):
            plt.text(
                x + 0.5,
                y + 0.5,
                "{:.0f}".format(df.iloc[y, x]),
                color="w",
                horizontalalignment="center",
                verticalalignment="center",
            )
    plt.yticks(np.arange(0.5, len(df.index), 1), df.index)
    plt.xticks(np.arange(0.5, len(df.columns), 1), df.columns, rotation=90)
    plt.colorbar(heatmap)
    plt.ylabel(y_label)
    plt.xlabel(x_label)
    return fig


@PlotRegister.register()
@manage_matplotlib_context()
def scatter(df, x_label, y_label) -> str:
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
    color = config["html"]["style"]["primary_color"].get(str)
    scatter_threshold = config["plot"]["scatter_threshold"].get(int)

    plt.xlabel(x_label)
    plt.ylabel(y_label)

    figure, ax = plt.subplots()

    series1 = df[x_label]
    series2 = df[y_label]
    if len(series1) > scatter_threshold:
        cmap = sns.light_palette(color, as_cmap=True)
        ax.hexbin(series1, series2, gridsize=15, cmap=cmap)
    else:
        ax.scatter(series1, series2, color=color)
    return figure


@PlotRegister.register()
@manage_matplotlib_context()
def pie_chart(data):
    def func(pct, allvals):
        absolute = int(pct / 100.0 * np.sum(allvals))
        return "{:.1f}%\n({:d})".format(pct, absolute)

    figure, ax = plt.subplots()
    wedges, _, _ = ax.pie(
        data, autopct=lambda pct: func(pct, data), textprops=dict(color="w")
    )
    plt.legend(wedges, data.index.values, loc="upper right")

    return figure


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


@PlotRegister.register()
@manage_matplotlib_context()
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
        color=hex_to_rgb(config["html"]["style"]["primary_color"].get(str)),
        fontsize=get_font_size(data) / 20 * 16,
        sparkline=False,
        labels=labels,
    )
    return plt.gcf()


@PlotRegister.register()
@manage_matplotlib_context()
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
        color=hex_to_rgb(config["html"]["style"]["primary_color"].get(str)),
        fontsize=get_font_size(data),
        labels=labels,
    )
    for ax0 in plt.gcf().get_axes():
        ax0.grid(False)

    return plt.gcf()


@PlotRegister.register()
@manage_matplotlib_context()
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
    return plt.gcf()


@PlotRegister.register()
@manage_matplotlib_context()
def missing_dendrogram(data: pd.DataFrame) -> str:
    """Generate a dendrogram plot for missing values.

    Args:
      data: Pandas DataFrame to generate missing values dendrogram plot from.

    Returns:
      The resulting missing values dendrogram plot encoded as a string.

    """
    missingno.dendrogram(data, fontsize=get_font_size(data) * 2.0)
    return plt.gcf()


@PlotRegister.register()
@manage_matplotlib_context()
def qq_plot(quantiles, dist=stats.norm) -> Figure:
    theoretical_percentiles, quantiles = zip(
        *sorted(quantiles.items(), key=lambda item: item[0])
    )
    if isinstance(dist, str):
        if dist == "normal":
            dist = stats.norm
        elif dist == "uniform":
            dist = stats.uniform

    sample_quantiles = quantiles
    q25 = stats.scoreatpercentile(sample_quantiles, 25)
    q75 = stats.scoreatpercentile(sample_quantiles, 75)

    # if theoretical_percentiles is None:
    # nobs = len(quantiles)
    #     theoretical_percentiles = np.arange(1., nobs + 1) / (nobs + 1)
    theoretical_quantiles = dist.ppf(theoretical_percentiles)

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_xmargin(0.02)
    ax.plot(theoretical_quantiles, sample_quantiles, "o")

    # line
    theoretical_quartiles = dist.ppf([0.25, 0.75])
    m = (q75 - q25) / np.diff(theoretical_quartiles)
    b = q25 - m * theoretical_quartiles[0]
    ax.plot(theoretical_quantiles, m * theoretical_quantiles + b, "-")

    ax.set_xlabel("Theoretical Quantiles")
    ax.set_ylabel("Sample Quantiles")

    return fig


@PlotRegister.register()
@manage_matplotlib_context()
def boxplot(label, min, q1, med, q3, max):
    # https://stackoverflow.com/questions/23655798/matplotlib-boxplot-using-precalculated-summary-statistics
    stats = [
        {
            "label": label,
            "med": med,
            "q1": q1,
            "q3": q3,
            "whislo": min,
            "whishi": max,
            "fliers": [],
        }
    ]

    fig, axes = plt.subplots()
    axes.bxp(stats)
    return fig


@PlotRegister.register()
@manage_matplotlib_context()
def kde(data):
    sns.kdeplot(data)
    return plt.gcf()
