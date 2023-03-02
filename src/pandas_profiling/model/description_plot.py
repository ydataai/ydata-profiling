from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from typing import Any, List, Optional

import numpy as np
import pandas as pd
from pandas_profiling.model.description_target import TargetDescription


@dataclass
class BasePlotDescription(metaclass=ABCMeta):
    """Base class for plot description.

    Attributes:
        data_col_name (str): Name of data column.
        target_col_name (str or None): Name of target column.
        data_col (Any): Column with data values.
        target_description (TargetDescription or None): Description of target column,
            if exists.
    """

    data_col_name: str
    data_col: Any
    target_description: Optional[TargetDescription]

    def __init__(
        self,
        data_col_name: str,
        data_col: Any,
        target_description: Optional[TargetDescription],
    ) -> None:
        """Setup basic parameters for plot description.s

        Args:
            data_col_name (str): Name of data column.
            data_col (Any): Column with data values.
            target_col_name (str or None): Name of target column.
        """
        self.data_col_name = data_col_name
        self.data_col = data_col
        self.target_description = target_description

    @property
    def target_col_name(self) -> Optional[str]:
        if self.target_description:
            return self.target_description.name
        return None

    @property
    def p_target_value(self) -> Optional[int]:
        """Positive target values if target exists. None otherwise."""
        if self.target_description:
            return self.target_description.bin_positive
        return None

    @property
    def n_target_value(self) -> Optional[int]:
        """Negative target values if target exists. None otherwise."""
        if self.target_description:
            return self.target_description.bin_negative
        return None

    def is_supervised(self) -> bool:
        """Return, if plot should be plotted as supervised, or not.
        Plot is supervised, if target description is not None."""
        return (
            self.target_description is not None
            and self.target_description.name != self.data_col_name
        )


class CategoricPlotDescription(BasePlotDescription):
    """Base class for categorical plot description.

    Attributes:
        distribution (pd.DataFrame): Distribution DataFrame preprocessed for plotting.
        log_odds (pd.DataFrame or None): Log2odds DataFrame preprocessed for plotting.
    """

    __distribution: pd.DataFrame
    __log_odds: Optional[pd.DataFrame] = None

    count_col_name: str = "count"
    log_odds_col_name: str = "log_odds"

    log_odds_text_col: str = "text_position"

    def __init__(
        self,
        data_col_name: str,
        data_col: Any,
        target_description: Optional[TargetDescription],
    ) -> None:
        super().__init__(data_col_name, data_col, target_description)
        distribution = self._generate_distribution()
        self.__validate_distribution(distribution)

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

    @abstractmethod
    def _generate_distribution(self) -> pd.DataFrame:
        """Generate distribution of variable.
        Distribution contains following columns:
            self.data_col_name: column with categories
            self.target_col_name: column with target binary values
            self.count_col_name: column with counts.
        Distribution DataFrame should contain all data_col and target_col combinations,
        even if count is 0.

        Examples:
            col_name,       target_name,    count
            1               0               10
            1               1               5
            2               0               8
            2               1               0
        """
        pass

    def __generate_log_odds(self):
        """Generates log2 odds preprocessed DataFrame based on distribution."""
        log_odds = pd.pivot_table(
            self.distribution,
            values=self.count_col_name,
            index=self.data_col_name,
            columns=self.target_col_name,
            sort=False,
        ).reset_index()
        log_odds.columns.name = ""

        # there is possibility, that positive, or negative values will not be present
        if not self.p_target_value in log_odds:
            log_odds[self.p_target_value] = 0
        if not self.n_target_value in log_odds:
            log_odds[self.n_target_value] = 0
        # counts log2 odds
        # TODO change to support multiple values
        log_odds["log_odds"] = round(
            np.log2(log_odds[self.p_target_value] / log_odds[self.n_target_value]),
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

    def __validate_distribution(self, distribution: pd.DataFrame) -> None:
        """Validate and set distribution DataFrame.
        - check if there are all needed columns
        - if report is supervised, generate log_odds

        Args:
            distribution (pd.DataFrame) : DataFrame, we want to validate.
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


class TextPlotDescription(BasePlotDescription):
    """Class to describe word cloud for text format data.

    Attributes:
        words_counts (pd.DataFrame): Sorted words and counts of those words.
    """

    _words_counts: pd.DataFrame

    def __init__(
        self,
        data_col_name: str,
        data_col: Any,
        target_description: Optional[TargetDescription],
    ) -> None:
        super().__init__(data_col_name, data_col, target_description)
        if self.target_description:
            self._words_counts = self.get_word_counts_supervised()
        else:
            self._words_counts = self.get_word_counts(self.data_col).to_frame(
                name=self.count_col_name
            )

    @property
    def count_col_name(self) -> str:
        """Name of column with absolute count of word."""
        return "count"

    @property
    def positive_col_name(self) -> str:
        """Name of column with count of word for positive target."""
        return "positive"

    @property
    def negative_col_name(self) -> str:
        """Name of column with count of word for negative target."""
        return "negative"

    @property
    def words_counts(self) -> pd.DataFrame:
        return self._words_counts

    @abstractmethod
    def get_word_counts(self, data: Any) -> pd.Series:
        """Generate word counts for input series.

        Returns:
            Series with unique words as index and the computed frequency as value.
        """
        pass

    @abstractmethod
    def get_word_counts_supervised(self) -> pd.DataFrame:
        """Generate word counts for supervised report.
        Splits data by target."""
        pass
