from dataclasses import dataclass
from typing import Optional

import numpy as np
from pandas_profiling.model.description_target import TargetDescription

import pandas as pd


@dataclass
class BasePlotDescription:
    """Base class for plot description.

    Attributes
    ----------
    data_col_name : str
        Name of data column.
    target_col_name : str or None
        Name of target column.
    count_col_name : str
        Name of count column in preprocessed DataFrames.
    log_odds_col_name : str
        Name of log2odds column in log_odds DataFrame.
    distribution : pd.DataFrame
        Distribution DataFrame preprocessed for plotting.
    log_odds : pd.DataFrame or None
        Log2odds DataFrame preprocessed for plotting.
    """

    data_col_name: str
    target_description: Optional[TargetDescription]

    __distribution: pd.DataFrame
    __log_odds: Optional[pd.DataFrame] = None

    count_col_name: str = "count"
    log_odds_col_name: str = "log_odds"

    log_odds_color: str = "green"
    log_odds_text_col: str = "text_position"

    def __init__(
        self,
        data_col_name: str,
        target_description: Optional[TargetDescription],
    ) -> None:
        """Setup basic parameters for plot description.s

        Parameters
        ----------
        data_col_name: str
            Name of data column.
        target_col_name: str or None
            Name of target column.
        target_positive_value : str or None
            Positive value of target column, if target column is set.
        target_negative_value : str or None
            Negative value of target column, if target column is set.
        """
        self.data_col_name = data_col_name
        self.target_description = target_description

    @property
    def target_col_name(self) -> Optional[str]:
        if self.target_description:
            return self.target_description.name
        return None

    @property
    def p_target_value(self) -> Optional[str]:
        if self.target_description:
            return self.target_description.positive_values[0]
        return None

    @property
    def n_target_value(self) -> Optional[str]:
        if self.target_description:
            return self.target_description.negative_values[0]
        return None

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
            raise ValueError(
                "Distribution not set at '{}' variable.".format(self.data_col_name)
            )
        return self.__distribution

    @property
    def log_odds(self) -> Optional[pd.DataFrame]:
        """Returns DataFrame with relative log2odds for data column.
        format:
            col_name,   log_odds
            male        -2
            female      2
        """
        return self.__log_odds

    def is_supervised(self) -> bool:
        """Return, if plot should be plotted as supervised, or not.
        Plot is supervised, if target description is not None."""
        return (
            self.target_description is not None
            and self.target_description.name != self.data_col_name
        )

    def __generate_log_odds(self):
        """Generates log2 odds preprocessed DataFrame based on distribution."""
        log_odds = pd.pivot_table(
            self.distribution,
            values=self.count_col_name,
            index=self.data_col_name,
            columns=self.target_description.name,
            sort=False,
        ).reset_index()
        log_odds.columns.name = ""
        # counts log2 odds
        # TODO change to support multiple values
        log_odds["log_odds"] = round(
            np.log2(
                log_odds[self.target_description.positive_values[0]]
                / log_odds[self.target_description.negative_values[0]]
            ),
            2,
        )
        # replace all special values with 0
        log_odds.fillna(0, inplace=True)
        log_odds.replace([np.inf, -np.inf], 0, inplace=True)

        # add text position for log2odds
        log_odds[self.log_odds_text_col] = "left"
        log_odds.loc[
            log_odds[self.log_odds_col_name] < 0, self.log_odds_text_col
        ] = "right"
        self.__log_odds = log_odds

    def _set_distribution(self, distribution: pd.DataFrame) -> None:
        """Validate and set distribution DataFrame.
        - check if there are all needed columns
        """
        if not isinstance(distribution, pd.DataFrame):
            raise ValueError("Preprocessed plot must be pd.DataFrame instance.")
        self.__check_columns(distribution)
        self.__distribution = distribution.reset_index(drop=True)

        # generate log_odds just for supervised report
        if self.is_supervised():
            self.__generate_log_odds()

    def __check_columns(self, df: pd.DataFrame):
        """Checks if df contains all columns (data_col, target_col, count_col)."""
        if self.data_col_name not in df:
            raise ValueError(
                "Data column '{}' not in DataFrame.".format(self.data_col_name)
            )
        if self.is_supervised() and (self.target_description.name not in df):
            raise ValueError(
                "Target column '{}' not in DataFrame.".format(
                    self.target_description.name
                )
            )
        if self.count_col_name not in df:
            raise ValueError(
                "Count column not in DataFrame. '{}'".format(self.data_col_name)
            )
