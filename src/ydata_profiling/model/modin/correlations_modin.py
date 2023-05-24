"""Correlations between variables."""
import itertools
from typing import Callable, Optional

import numpy as np
import pandas as pd

from ydata_profiling.config import Settings
from ydata_profiling.model.correlations import (
    Auto,
    Cramers,
    Kendall,
    Pearson,
    PhiK,
    Spearman,
)
from ydata_profiling.model.modin.discretize_modin import DiscretizationType, Discretizer
from ydata_profiling.model.pandas.correlations_pandas import (
    _pairwise_cramers,
    _pairwise_spearman,
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
    threshold = config.categorical_maximum_correlation_distinct
    numerical_columns = [
        key
        for key, value in summary.items()
        if value["type"] in {"Numeric", "TimeSeries"} and value["n_distinct"] > 1
    ]
    categorical_columns = [
        key
        for key, value in summary.items()
        if value["type"] in {"Categorical", "Boolean"}
        and 1 < value["n_distinct"] <= threshold
    ]

    if len(numerical_columns + categorical_columns) <= 1:
        return None

    df_discretized = Discretizer(
        DiscretizationType.UNIFORM, n_bins=config.correlations["auto"].n_bins
    ).discretize_dataframe(df)
    columns_tested = numerical_columns + categorical_columns
    correlation_matrix = modin.DataFrame(
        np.ones((len(columns_tested), len(columns_tested))),
        index=columns_tested,
        columns=columns_tested,
    )
    for col_1_name, col_2_name in itertools.combinations(columns_tested, 2):
        method = (
            _pairwise_spearman
            if col_1_name and col_2_name not in categorical_columns
            else _pairwise_cramers
        )

        def f(col_name: str, method: Callable) -> pd.Series:
            return (
                df_discretized
                if col_name in numerical_columns and method is _pairwise_cramers
                else df
            )

        score = method(
            f(col_1_name, method)[col_1_name], f(col_2_name, method)[col_2_name]
        )
        (
            correlation_matrix.loc[col_1_name, col_2_name],
            correlation_matrix.loc[col_2_name, col_1_name],
        ) = (score, score)

    return correlation_matrix
