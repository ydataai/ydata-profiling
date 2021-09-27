import pandas as pd

from pandas_profiling.config import Settings
from pandas_profiling.model.missing import (
    missing_bar,
    missing_dendrogram,
    missing_heatmap,
    missing_matrix,
)
from pandas_profiling.visualisation.missing import (
    plot_missing_bar,
    plot_missing_dendrogram,
    plot_missing_heatmap,
    plot_missing_matrix,
)


@missing_bar.register
def pandas_missing_bar(config: Settings, df: pd.DataFrame) -> str:
    return plot_missing_bar(config, df)


@missing_matrix.register
def pandas_missing_matrix(config: Settings, df: pd.DataFrame) -> str:
    return plot_missing_matrix(config, df)


@missing_heatmap.register
def pandas_missing_heatmap(config: Settings, df: pd.DataFrame) -> str:
    return plot_missing_heatmap(config, df)


@missing_dendrogram.register
def pandas_missing_dendrogram(config: Settings, df: pd.DataFrame) -> str:
    return plot_missing_dendrogram(config, df)
