"""Correlations between variables."""
from typing import Optional

import pandas as pd

from pandas_profiling.config import Settings
from pandas_profiling.model.correlations import Kendall, Pearson, Spearman


@Spearman.compute.register(Settings, pd.DataFrame, dict)
def pandas_spearman_compute(
    config: Settings, df: pd.DataFrame, summary: dict
) -> Optional[pd.DataFrame]:
    return df.corr(method="spearman")


@Pearson.compute.register(Settings, pd.DataFrame, dict)
def pandas_pearson_compute(
    config: Settings, df: pd.DataFrame, summary: dict
) -> Optional[pd.DataFrame]:
    return df.corr(method="pearson")


@Kendall.compute.register(Settings, pd.DataFrame, dict)
def pandas_kendall_compute(
    config: Settings, df: pd.DataFrame, summary: dict
) -> Optional[pd.DataFrame]:
    return df.corr(method="kendall")
