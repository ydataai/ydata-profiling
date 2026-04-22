from typing import Any, List, Optional

import numpy as np
from pyspark.sql import DataFrame

from ydata_profiling.config import Settings
from ydata_profiling.visualisation.missing import (
    plot_missing_bar,
    plot_missing_heatmap,
    plot_missing_matrix,
)


class MissingnoBarSparkPatch:
    """
    Adapter class to enable missingno library compatibility with Spark DataFrames.
    
    The missingno library's visualization functions internally call isnull().sum() 
    on dataframes. For Spark DataFrames, we pre-compute the null counts and wrap
    them in this adapter to provide the expected interface.
    
    Note: This is a workaround for missingno's lack of separation between
    data preprocessing and visualization. See:
    https://github.com/ResidentMario/missingno/issues/119
    """

    def __init__(
        self, 
        df: DataFrame, 
        columns: Optional[List[str]] = None, 
        original_df_size: Optional[int] = None
    ):
        self.df = df
        self.columns = columns
        self.original_df_size = original_df_size

    def isnull(self) -> "MissingnoBarSparkPatch":
        """Returns self to enable chained .isnull().sum() calls."""
        return self

    def sum(self) -> DataFrame:
        """Returns the pre-computed null counts dataframe."""
        return self.df

    def __len__(self) -> Optional[int]:
        """Returns the original dataframe size."""
        return self.original_df_size


def missing_bar(config: Settings, df: DataFrame) -> str:
    """Generate a missing values bar chart for Spark DataFrame.
    
    :param config: Report settings
    :param df: Spark DataFrame
    :return: HTML string of the bar chart
    """
    import pyspark.sql.functions as F

    data_nan_counts = (
        df.agg(
            *[F.count(F.when(F.isnull(c) | F.isnan(c), c)).alias(c) for c in df.columns]
        )
        .toPandas()
        .squeeze(axis="index")
    )

    return plot_missing_bar(
        config, notnull_counts=data_nan_counts, columns=df.columns, nrows=df.count()
    )


def missing_matrix(config: Settings, df: DataFrame) -> str:
    """Generate a missing values matrix visualization for Spark DataFrame.
    
    :param config: Report settings
    :param df: Spark DataFrame
    :return: HTML string of the matrix visualization
    """
    df = MissingnoBarSparkPatch(df, columns=df.columns, original_df_size=df.count())
    return plot_missing_matrix(
        config,
        columns=df.columns,
        notnull=df.notnull().values,
        nrows=len(df),
    )


def missing_heatmap(config: Settings, df: DataFrame) -> str:
    """Generate a missing values heatmap for Spark DataFrame.
    
    :param config: Report settings
    :param df: Spark DataFrame
    :return: HTML string of the heatmap
    """
    df = MissingnoBarSparkPatch(df, columns=df.columns, original_df_size=df.count())

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
