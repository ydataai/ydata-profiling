from typing import Any, Dict, List, Tuple

import numpy as np
import pandas as pd
from pandas_profiling.config import Target
from pandas_profiling.model.description_target import TargetDescription, describe_target


class TargetDescriptionPandas(TargetDescription):
    series: pd.Series
    series_binary: pd.Series

    def __init__(
        self,
        target_config: Target,
        series: pd.Series,
    ) -> None:
        series = series.astype(str)
        super().__init__(target_config, series)

    def _infer_target_values(self) -> Tuple[List[str], List[str]]:
        """Infer positive and negative values."""
        unique_vals = self.series.dropna().unique()
        # user defined positive values
        if self.config.positive_values is not None:
            positive_vals = self.config.positive_values
        # positive values are not defined
        else:
            positive_vals = []
            for value in unique_vals:
                if str(value).lower() in self.config.inferred_positive_values:
                    positive_vals.append(value)

            if len(positive_vals) == 0:
                positive_vals.append(unique_vals[0])

        negative_vals = np.setdiff1d(unique_vals, positive_vals)
        return positive_vals, list(negative_vals)

    def _get_bin_target(self) -> pd.Series:
        _bin_target = self.series.copy()
        _bin_target.replace(self.positive_values, 1, inplace=True)
        _bin_target.replace(self.negative_values, -1, inplace=True)
        return _bin_target

    def _get_advanced_description(self) -> Dict[str, Any]:
        _desc = {}
        _desc["target_mean"] = self.series_binary.mean()

        return _desc

    @property
    def n_positive_vals(self) -> int:
        return self.series[self.series.isin(self.positive_values)].count()

    @property
    def p_positive_vals(self) -> float:
        return self.n_positive_vals / self.series.size

    @property
    def n_negative_vals(self) -> int:
        return self.series[self.series.isin(self.negative_values)].count()

    @property
    def p_negative_vals(self) -> float:
        return self.n_negative_vals / self.series.size


@describe_target.register
def describe_target_pandas(
    config: Target,
    data_frame: pd.DataFrame,
) -> TargetDescription:
    if config.col_name is None:
        raise ValueError("Target not defined.")
    series = data_frame[config.col_name]
    return TargetDescriptionPandas(config, series)
