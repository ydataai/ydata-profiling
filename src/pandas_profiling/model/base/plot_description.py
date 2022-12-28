from typing import Optional
import pandas as pd


class BasePlotDescription:
    def __init__(
        self,
        preprocessed_plot: pd.DataFrame,
        data_col_name: str,
        target_col_name: Optional[str],
    ) -> None:
        """
        preprocessed_plot: pd.DataFrame with 2 or 3 columns (data_col, target_col or None, count)
            in format:
                col_name,   target_name,    count
                1           0               10
                1           1               5
                2           0               8
                ...
        data_col: str
            column name of data col (needs to be in preprocessed plot)
        target_col: str | None
            column name of target col (if not None, needs to be in preprocessed plot)
        """
        self._preprocessed_plot = preprocessed_plot
        self._data_col = data_col_name
        self._target_col = target_col_name
        # TODO check, if the df is valid

    @property
    def preprocessed_plot(self) -> pd.DataFrame:
        """Returns preprocessed dataframe for plotting"""
        return self._preprocessed_plot

    @property
    def target_col(self):
        return self._target_col

    @property
    def data_col(self):
        return self._data_col


class PlotDescriptionCategorical(BasePlotDescription):
    pass
