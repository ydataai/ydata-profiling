"""Plotting functions for the missing values diagrams"""
from functools import singledispatch
from typing import Union

from matplotlib import pyplot as plt
from missingno import missingno

from pandas_profiling.config import config
from pandas_profiling.model.dataframe_wrappers import (
    GenericDataFrame,
    PandasDataFrame,
    SparkDataFrame,
)
from pandas_profiling.visualisation.context import manage_matplotlib_context
from pandas_profiling.visualisation.utils import hex_to_rgb, plot_360_n0sc0pe


def get_font_size(data: GenericDataFrame):
    """Calculate font size based on number of columns

    Args:
        data: DataFrame

    Returns:
        Font size for missing values plots.
    """
    max_label_length = max([len(label) for label in data.columns])

    if len(data.columns) < 20:
        font_size: Union[int, float] = 13
    elif 20 <= len(data.columns) < 40:
        font_size = 12
    elif 40 <= len(data.columns) < 60:
        font_size = 10
    else:
        font_size = 8

    font_size *= min(1.0, 20.0 / max_label_length)
    return font_size


@singledispatch
@manage_matplotlib_context()
def missing_matrix(data) -> str:
    raise NotImplementedError("method is not implemented for datatype")


@missing_matrix.register(PandasDataFrame)
@manage_matplotlib_context()
def _missing_matrix_pandas(data: PandasDataFrame) -> str:
    """Generate missing values matrix plot

    Args:
      data: Pandas DataFrame to generate missing values matrix from.

    Returns:
      The resulting missing values matrix encoded as a string.
    """
    labels = config["plot"]["missing"]["force_labels"].get(bool)
    missingno.matrix(
        data.get_pandas_df(),
        figsize=(10, 4),
        color=hex_to_rgb(config["html"]["style"]["primary_color"].get(str)),
        fontsize=get_font_size(data) / 20 * 16,
        sparkline=False,
        labels=labels,
    )
    plt.subplots_adjust(left=0.1, right=0.9, top=0.7, bottom=0.2)
    return plot_360_n0sc0pe(plt)


@singledispatch
@manage_matplotlib_context()
def missing_bar(data) -> str:
    raise NotImplementedError("method is not implemented for datatype")


@missing_bar.register(PandasDataFrame)
@manage_matplotlib_context()
def _missing_bar_pandas(data: PandasDataFrame) -> str:
    """Generate missing values bar plot.

    Args:
      data: Pandas DataFrame to generate missing values bar plot from.

    Returns:
      The resulting missing values bar plot encoded as a string.
    """
    labels = config["plot"]["missing"]["force_labels"].get(bool)
    missingno.bar(
        data.get_pandas_df(),
        figsize=(10, 5),
        color=hex_to_rgb(config["html"]["style"]["primary_color"].get(str)),
        fontsize=get_font_size(data),
        labels=labels,
    )
    for ax0 in plt.gcf().get_axes():
        ax0.grid(False)
    plt.subplots_adjust(left=0.1, right=0.9, top=0.8, bottom=0.3)

    return plot_360_n0sc0pe(plt)


@missing_bar.register(SparkDataFrame)
@manage_matplotlib_context()
def _missing_bar_spark(data: SparkDataFrame) -> str:
    """Generate missing values bar plot.

    Args:
      data: Pandas DataFrame to generate missing values bar plot from.

    Returns:
      The resulting missing values bar plot encoded as a string.
    """
    labels = config["plot"]["missing"]["force_labels"].get(bool)

    class MissingnoBarSparkPatch:
        """
        Technical Debt :
        This is a monkey patching object that allows usage of the library missingno as is for spark dataframes.
        This is because missingno library's bar function always applies a isnull().sum() on dataframes in the visualisation
        function, instead of allowing just values counts as an entry point. Thus, in order to calculate the
        missing values dataframe in spark, we compute it first, then wrap it in this MissingnoBarSparkPatch object which
        will be unwrapped by missingno and return the pre-computed value counts.

        The best fix to this currently terrible patch is to submit a PR to missingno to separate preprocessing function
        (compute value counts from df) and visualisation functions such that we can call the visualisation directly.
        Unfortunately, the missingno library people have not really responded to our issues on gitlab.
        See https://github.com/ResidentMario/missingno/issues/119.
        We could also fork the missingno library and implement some of the code in our database, but that feels
        like bad practice as well.
        """

        def __init__(self, df, original_df_size=None):
            self.df = df
            self.original_df_size = original_df_size

        def isnull(self):
            """
            This patches the .isnull().sum() function called by missingno library
            """
            return self  # return self to patch .sum() function

        def sum(self):
            """
            This patches the .sum() function called by missingno library
            """
            return self.df  # return unwrapped dataframe

        def __len__(self):
            """
            This patches the len(df) function called by missingno library
            """
            return self.original_df_size

    # pre-compute the nan counts in spark
    data_nan_counts = data.nan_counts()

    missingno.bar(
        MissingnoBarSparkPatch(df=data_nan_counts, original_df_size=data.n_rows),
        figsize=(10, 5),
        color=hex_to_rgb(config["html"]["style"]["primary_color"].get(str)),
        fontsize=get_font_size(data),
        labels=labels,
    )

    for ax0 in plt.gcf().get_axes():
        ax0.grid(False)
    plt.subplots_adjust(left=0.1, right=0.9, top=0.8, bottom=0.3)

    return plot_360_n0sc0pe(plt)


@singledispatch
@manage_matplotlib_context()
def missing_heatmap(data) -> str:
    raise NotImplementedError("method is not implemented for datatype")


@missing_heatmap.register(PandasDataFrame)
@manage_matplotlib_context()
def _missing_heatmap_pandas(data: PandasDataFrame) -> str:
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
        data.get_pandas_df(),
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
@singledispatch
def missing_dendrogram(data) -> str:
    raise NotImplementedError("method is not implemented for datatype")


@manage_matplotlib_context()
@missing_dendrogram.register(PandasDataFrame)
def _missing_dendrogram_pandas(data: PandasDataFrame) -> str:
    """Generate a dendrogram plot for missing values.

    Args:
      data: Pandas DataFrame to generate missing values dendrogram plot from.

    Returns:
      The resulting missing values dendrogram plot encoded as a string.

    """
    missingno.dendrogram(data.get_pandas_df(), fontsize=get_font_size(data) * 2.0)
    plt.subplots_adjust(left=0.1, right=0.9, top=0.7, bottom=0.2)
    return plot_360_n0sc0pe(plt)
