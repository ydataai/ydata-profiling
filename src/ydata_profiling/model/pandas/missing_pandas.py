import numpy as np
import pandas as pd

from ydata_profiling.config import Settings
from ydata_profiling.visualisation.missing import (
    plot_missing_bar,
    plot_missing_heatmap,
    plot_missing_matrix,
)


def missing_bar(config: Settings, df: pd.DataFrame) -> str:
    notnull_counts = len(df) - df.isnull().sum()
    return plot_missing_bar(
        config,
        notnull_counts=notnull_counts,
        nrows=len(df),
        columns=list(df.columns),
    )


def missing_matrix(config: Settings, df: pd.DataFrame) -> str:
    return plot_missing_matrix(
        config,
        columns=list(df.columns),
        notnull=df.notnull().values,
        nrows=len(df),
    )


def missing_heatmap(config: Settings, df: pd.DataFrame) -> str:
    # Remove completely filled or completely empty variables.
    columns = [i for i, n in enumerate(np.var(df.isnull(), axis="rows")) if n > 0]
    df = df.iloc[:, columns]

    # Create and mask the correlation matrix. Construct the base heatmap.
    corr_mat = df.isnull().corr()
    mask = np.zeros_like(corr_mat)
    mask[np.triu_indices_from(mask)] = True
    return plot_missing_heatmap(
        config, corr_mat=corr_mat, mask=mask, columns=list(df.columns)
    )
