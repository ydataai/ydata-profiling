from typing import Any, Dict, Optional
import pandas as pd
from pandas_profiling.model.base.serializable import SerializableInterface


class BasePlotDescription(SerializableInterface):
    count_col_name = 'count'

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
        preprocessed_plot.reset_index(inplace=True, drop=True)
        self._preprocessed_plot = preprocessed_plot
        self._data_col = data_col_name
        self._target_col = target_col_name
        # TODO check, if the df is valid

    @property
    def preprocessed_plot(self) -> pd.DataFrame:
        """Returns preprocessed dataframe for plotting"""
        return self._preprocessed_plot.copy()

    @property
    def target_col(self):
        return self._target_col

    @property
    def data_col(self):
        return self._data_col

    @classmethod
    def prepare_data_col(cls, data_col: pd.Series) -> str:
        """Fill col name, if None.

        Returns column name
        """
        if data_col.name is None:
            data_col.name = "data_col"
        return str(data_col.name)

    @classmethod
    def prepare_target_col(cls, target_col: Optional[pd.Series]):
        if target_col is None:
            return None
        if target_col.name is None:
            target_col.name = "target_col"
        return str(target_col.name)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "preprocessed_plot": self.preprocessed_plot,
            "target_col": self.target_col,
            "data_col": self.data_col,
        }
