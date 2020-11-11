"""Plotting functions for the missing values diagrams"""
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from missingno import missingno

from pandas_profiling.config import config
from pandas_profiling.visualisation.context import manage_matplotlib_context
from pandas_profiling.visualisation.utils import hex_to_rgb, plot_360_n0sc0pe


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
    plt.subplots_adjust(left=0.1, right=0.9, top=0.7, bottom=0.2)
    return plot_360_n0sc0pe(plt)


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
    plt.subplots_adjust(left=0.1, right=0.9, top=0.8, bottom=0.3)

    return plot_360_n0sc0pe(plt)

@manage_matplotlib_context()
def missing_bar2(data: pd.DataFrame) -> str:
    """Generate missing values bar plot.

    Args:
      data: Pandas DataFrame to generate missing values bar plot from.

    Returns:
      The resulting missing values bar plot encoded as a string.
    """
    labels = config["plot"]["missing2"]["force_labels"].get(bool)
    data = ((data.notnull()).astype('int')).where(lambda a:a==0,np.nan)
    missingno.bar(
        data,
        figsize=(10, 5),
        color=hex_to_rgb(config["html"]["style"]["primary_color"].get(str)),
        fontsize=get_font_size(data),
        labels=labels,
    )
    for ax0 in plt.gcf().get_axes():
        ax0.grid(False)
    plt.subplots_adjust(left=0.1, right=0.9, top=0.8, bottom=0.3)

    return plot_360_n0sc0pe(plt)


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

    if len(data.columns) > 40:
        plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.3)
    else:
        plt.subplots_adjust(left=0.2, right=0.9, top=0.8, bottom=0.3)

    return plot_360_n0sc0pe(plt)


@manage_matplotlib_context()
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
