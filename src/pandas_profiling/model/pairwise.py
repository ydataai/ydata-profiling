from typing import Any, Dict, List, Tuple

import pandas as pd

from pandas_profiling.config import Settings
from pandas_profiling.visualisation.plot import scatter_pairwise


def get_scatter_tasks(
    config: Settings, continuous_variables: list
) -> List[Tuple[Any, Any]]:
    if not config.interactions.continuous:
        return []

    targets = config.interactions.targets
    if len(targets) == 0:
        targets = continuous_variables

    tasks = [(x, y) for y in continuous_variables for x in targets]
    return tasks


def get_scatter_matrix(
    config: Settings,
    df: pd.DataFrame,
    continuous_variables: list,
    tasks: List[Tuple[Any, Any]],
) -> dict:
    scatter_matrix: Dict[Any, Dict[Any, Any]] = {}
    for x, y in tasks:
        if x not in scatter_matrix:
            scatter_matrix[x] = {}
        if y not in scatter_matrix[x]:
            scatter_matrix[x][y] = {}

        if x in continuous_variables:
            if y == x:
                df_temp = df[[x]].dropna()
            else:
                df_temp = df[[x, y]].dropna()
            scatter_matrix[x][y] = scatter_pairwise(
                config, df_temp[x], df_temp[y], x, y
            )
        else:
            scatter_matrix[x][y] = ""

    return scatter_matrix
