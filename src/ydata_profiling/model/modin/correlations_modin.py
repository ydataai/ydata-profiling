"""Correlations between variables."""
from typing import Optional

from ydata_profiling.config import Settings
from ydata_profiling.model.correlations import (
    Auto,
    Cramers,
    Kendall,
    Pearson,
    PhiK,
    Spearman,
)
from ydata_profiling.model.pandas.correlations_pandas import (
    pandas_auto_compute,
    pandas_cramers_compute,
    pandas_kendall_compute,
    pandas_pearson_compute,
    pandas_phik_compute,
    pandas_spearman_compute,
)
from ydata_profiling.utils import modin


@Spearman.compute.register(Settings, modin.DataFrame, dict)
def modin_spearman_compute(
    config: Settings, df: modin.DataFrame, summary: dict
) -> Optional[modin.DataFrame]:
    return pandas_spearman_compute(config, df, summary)


@Pearson.compute.register(Settings, modin.DataFrame, dict)
def modin_pearson_compute(
    config: Settings, df: modin.DataFrame, summary: dict
) -> Optional[modin.DataFrame]:
    return pandas_pearson_compute(config, df, summary)


@Kendall.compute.register(Settings, modin.DataFrame, dict)
def modin_kendall_compute(
    config: Settings, df: modin.DataFrame, summary: dict
) -> Optional[modin.DataFrame]:
    return pandas_kendall_compute(config, df, summary)


@Cramers.compute.register(Settings, modin.DataFrame, dict)
def modin_cramers_compute(
    config: Settings, df: modin.DataFrame, summary: dict
) -> Optional[modin.DataFrame]:
    return pandas_cramers_compute(config, df, summary)


@PhiK.compute.register(Settings, modin.DataFrame, dict)
def modin_phik_compute(
    config: Settings, df: modin.DataFrame, summary: dict
) -> Optional[modin.DataFrame]:
    return pandas_phik_compute(config, df, summary)


@Auto.compute.register(Settings, modin.DataFrame, dict)
def modin_auto_compute(
    config: Settings, df: modin.DataFrame, summary: dict
) -> Optional[modin.DataFrame]:
    return pandas_auto_compute(config, df, summary)
