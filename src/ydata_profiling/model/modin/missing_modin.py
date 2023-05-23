from ydata_profiling.config import Settings
from ydata_profiling.model.missing import missing_bar
from ydata_profiling.model.pandas.missing_pandas import (
    pandas_missing_bar,
    pandas_missing_heatmap,
    pandas_missing_matrix,
)
from ydata_profiling.utils import modin


@missing_bar.register
def modin_missing_bar(config: Settings, df: modin.DataFrame) -> str:
    return pandas_missing_bar(config, df)


@missing_bar.register
def modin_missing_matrix(config: Settings, df: modin.DataFrame) -> str:
    return pandas_missing_matrix(config, df)


@missing_bar.register
def modin_missing_heatmap(config: Settings, df: modin.DataFrame) -> str:
    return pandas_missing_heatmap(config, df)
