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

    def __init__(
        self, df: DataFrame, columns: List[str] = None, original_df_size: int = None
    ):
        self.df = df
        self.columns = columns
        self.original_df_size = original_df_size

    def isnull(self) -> Any:
        """
        This patches the .isnull().sum() function called by missingno library
        """
        return self  # return self to patch .sum() function

    def sum(self) -> DataFrame:
        """
        This patches the .sum() function called by missingno library
        """
        return self.df  # return unwrapped dataframe

    def __len__(self) -> Optional[int]:
        """
        This patches the len(df) function called by missingno library
        """
        return self.original_df_size


def missing_bar(config: Settings, df: DataFrame) -> str:
    import pyspark.sql.functions as F

    # FIXME: move to univariate
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
    df = MissingnoBarSparkPatch(df, columns=df.columns, original_df_size=df.count())
    return plot_missing_matrix(
        config,
        columns=df.columns,
        notnull=df.notnull().values,
        nrows=len(df),
    )


def missing_heatmap(config: Settings, df: DataFrame) -> str:
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
