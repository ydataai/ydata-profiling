from dataclasses import dataclass
from typing import Any, Dict, Optional

import numpy as np
import pandas as pd


@dataclass
class BasePlotDescription:
    """Base class for all plot descriptions.

    Attributes
    ----------
    data_col_name : str
        Name of data column.
    target_col_name : str or None
        Name of target column.
    count_col_name : str
        Name of count column in preprocessed DataFrames.
    log_odds : pd.DataFrame
        Prepared data to plot log_odds plot for supervised plot.


    """

    __data_col_name: str
    __target_col_name: str
    __distribution: pd.DataFrame

    _count_col_name: str = "count"
    _log_odds_col_name: str = "log_odds"
    __log_odds: Optional[pd.DataFrame] = None

    def __init__(self, data_col: pd.Series, target_col: Optional[pd.Series]) -> None:
        """
        data_col: pd.Series
            data column
        target_col: pd.Series or None
            target column
        """

        self.__prepare_data_col(data_col)
        self.__prepare_target_col(target_col)

    @property
    def data_col_name(self) -> str:
        return self.__data_col_name

    @property
    def target_col_name(self) -> Optional[str]:
        return self.__target_col_name

    @property
    def count_col_name(self) -> str:
        return self._count_col_name

    @property
    def distribution(self) -> pd.DataFrame:
        """Returns preprocessed DataFrame for plotting

        distribution: pd.DataFrame with 2 or 3 columns (data_col, target_col or None, count)
        in format:
            col_name,   target_name,    count
            1           0               10
            1           1               5
            2           0               8
            ..."""
        if self.__distribution is None:
            raise ValueError(f"preprocessed plot not found in '{self.data_col_name}'")
        return self.__distribution.copy()

    @property
    def log_odds(self) -> pd.DataFrame:
        """Returns DataFrame with log odds for data column"""
        if self.__log_odds is None:
            raise ValueError(f"log_odds not found in '{self.data_col_name}'")
        return self.__log_odds

    @property
    def log_odds_col_name(self) -> str:
        """DataFrame with log odds information"""
        if self.__log_odds is None:
            self.__generate_log_odds()
        return self._log_odds_col_name

    def __prepare_data_col(self, data_col: pd.Series) -> None:
        """Fills col name, if None.

        Returns column name
        """
        if data_col.name is None:
            data_col.name = "data_col"
        self.__data_col_name = str(data_col.name)

    def __prepare_target_col(self, target_col: Optional[pd.Series]) -> None:
        if target_col is None:
            self.__target_col_name = None
            return None
        if target_col.name is None:
            target_col.name = "target_col"
        self.__target_col_name = str(target_col.name)

    def __check_columns(self, df: pd.DataFrame):
        """Checks if df contains all columns (data_col, target_col, count_col)
        and if columns ar in correct dtype"""
        if self.data_col_name not in df:
            raise ValueError("Data column not in DataFrame")
        if (self.target_col_name is not None) and (self.target_col_name not in df):
            raise ValueError(
                "Target column not in DataFrame in '{}'".format(self.data_col_name)
            )
        if self.count_col_name not in df:
            raise ValueError("Count column not in DataFrame")

        if self.target_col_name is not None:
            df[self.target_col_name] = df[self.target_col_name].astype(str)
        return df

    def __generate_log_odds(self):
        log_odds = pd.pivot_table(
            self.distribution,
            values=self.count_col_name,
            index=self.data_col_name,
            columns=self.target_col_name,
            sort=False,
        ).reset_index()
        log_odds.columns.name = ""
        # TODO replace '0' and '1'
        log_odds["log_odds"] = round(np.log2(log_odds["1"] / log_odds["0"]), 2)
        # replace all special values with 0
        log_odds.fillna(0, inplace=True)
        log_odds.replace([np.inf, -np.inf], 0, inplace=True)
        self.__log_odds = log_odds

    def _validate(self, distribution: pd.DataFrame) -> None:
        """Validates distribution DataFrame"""
        if not isinstance(distribution, pd.DataFrame):
            raise ValueError("Preprocessed plot must be pd.DataFrame instance.")
        self.__check_columns(distribution)
        self.__distribution = distribution.reset_index(drop=True)

        # generate log_odds just for supervised report
        if self.target_col_name is not None:
            self.__generate_log_odds()
