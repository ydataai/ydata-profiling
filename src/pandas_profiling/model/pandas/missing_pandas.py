from typing import Dict

import pandas as pd
from pandas_profiling.config import Settings
from pandas_profiling.model.data import ConfMatrixData
from pandas_profiling.model.missing import (
    MissingDescription,
    get_missing_description,
    missing_bar,
    missing_heatmap,
    missing_matrix,
)
from pandas_profiling.model.pandas.description_target_pandas import (
    TargetDescriptionPandas,
)
from pandas_profiling.visualisation.missing import (
    plot_missing_bar,
    plot_missing_heatmap,
    plot_missing_matrix,
)


class MissingDescriptionPandas(MissingDescription):
    def __init__(self, df: pd.DataFrame, target_description: TargetDescriptionPandas):
        missing_target: Dict[str, ConfMatrixData] = {}

        _target_name = "Target ({})".format(target_description.name)
        for col_name in df.columns:
            col_name = str(col_name)
            if col_name == target_description.name:
                continue
            # generate conf matrix for columns with missing values
            if df[col_name].isna().any():
                _missing_name = "Missing ({})".format(col_name)
                col_bin = df[col_name].isna()
                _df = target_description.series_binary.to_frame().join(
                    col_bin, how="left"
                )
                absolute_conf_matrix = pd.crosstab(
                    _df[target_description.name],
                    _df[col_name],
                    rownames=[_target_name],
                    colnames=[_missing_name],
                )
                relative_conf_matrix = pd.crosstab(
                    _df[target_description.name],
                    _df[col_name],
                    rownames=[_target_name],
                    colnames=[_missing_name],
                    normalize="index",
                )

                missing_target[col_name] = ConfMatrixData(
                    absolute_conf_matrix, relative_conf_matrix
                )

        super().__init__(missing_target)


@get_missing_description.register
def pandas_get_missing_description(
    config: Settings, df: pd.DataFrame, target_description: TargetDescriptionPandas
) -> MissingDescriptionPandas:
    return MissingDescriptionPandas(df, target_description)


@missing_bar.register
def pandas_missing_bar(config: Settings, df: pd.DataFrame) -> str:
    return plot_missing_bar(config, df)


@missing_matrix.register
def pandas_missing_matrix(config: Settings, df: pd.DataFrame) -> str:
    return plot_missing_matrix(config, df)


@missing_heatmap.register
def pandas_missing_heatmap(config: Settings, df: pd.DataFrame) -> str:
    return plot_missing_heatmap(config, df)
