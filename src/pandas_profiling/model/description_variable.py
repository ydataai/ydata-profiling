from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

import numpy as np
from pandas_profiling.config import Univariate
from pandas_profiling.model.description_target import TargetDescription

import pandas as pd


@dataclass
class VariableDescription(ABC):
    """Interface for variable description.

    Attributes:
        config (Univariate): Setting of variables description.
        data_col (Any): Column with data values.
        data_col_name (str): Name of data column.
    """

    @property
    @abstractmethod
    def config(self) -> Univariate:
        """Config of variables description."""
        pass

    @property
    @abstractmethod
    def data_col(self) -> Any:
        """Series with data."""
        pass

    @property
    @abstractmethod
    def data_col_name(self) -> str:
        """Name of data column."""
        pass


class VariableDescriptionSupervised(VariableDescription):
    """Interface for supervised variable description.
    Extension of VariableDescription.

    Attributes:
        target_description (TargetDescription): Description of target column.
        target_col_name (str): Name of target column.
        p_target_value (int): Positive value of target column.
        n_target_value (int): Negative value of target column.
    """

    @property
    @abstractmethod
    def target_description(self) -> TargetDescription:
        """Description of target column."""

    @property
    def target_col_name(self) -> str:
        return self.target_description.name

    @property
    def p_target_value(self) -> int:
        """Positive binary target value."""
        return self.target_description.bin_positive

    @property
    def n_target_value(self) -> int:
        """Negative binary target value."""
        return self.target_description.bin_negative


class CatDescription(VariableDescription):
    """Abstract class for categorical unsupervised variable description.
    Extension of VariableDescription

    Attributes:
        distribution (pd.DataFrame): Distribution DataFrame preprocessed for plotting.
        count_col_name (str): Column name for count column.
    """

    __distribution: pd.DataFrame
    count_col_name: str = "count"

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
        if not hasattr(self, "__distribution"):
            self.__validate_distribution()
        return self.__distribution

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

    def __validate_distribution(self) -> None:
        """Validate and set distribution DataFrame.
        - check if there are all needed columns
        - if report is supervised, generate log_odds

        Args:
            distribution (pd.DataFrame) : DataFrame, we want to validate.
        """
        distribution = self._generate_distribution()
        if not isinstance(distribution, pd.DataFrame):
            raise ValueError("Preprocessed plot must be pd.DataFrame instance.")
        self._check_columns(distribution)
        self.__distribution = distribution.reset_index(drop=True)

    def _check_columns(self, df: pd.DataFrame):
        """Checks if df contains all columns (data_col, target_col, count_col)."""
        if self.data_col_name not in df:
            raise ValueError(
                "Data column '{}' not in DataFrame.".format(self.data_col_name)
            )
        if self.count_col_name not in df:
            raise ValueError(
                "Count column not in DataFrame. '{}'".format(self.data_col_name)
            )


class CatDescriptionSupervised(CatDescription, VariableDescriptionSupervised):
    """Interface for supervised categorical variable description.
    Extension of CatDescription and VariableDescriptionSupervised.

    Attributes:
        log_odds (pd.DataFrame): Log2 odds DataFrame preprocessed for plotting.
        log_odds_col_name (str): Column name for count column.
    """

    __log_odds: pd.DataFrame
    log_odds_col_name: str = "log_odds_ratio"
    log_odds_text_col: str = "text_position"

    @property
    def log_odds(self) -> pd.DataFrame:
        """Returns DataFrame with relative log2odds for data column.
        format:
            col_name,   log_odds
            male        -2
            female      2
        """
        if not hasattr(self, "__log_odds"):
            self.__generate_log_odds_ratio()
        return self.__log_odds

    def __generate_log_odds_ratio(self):
        """Generates log2 odds ratio preprocessed DataFrame based on distribution.
        Compute odds for whole population and for every category.
        From that compute log odds ratio.
        """
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

        # Laplace smoothing for odds
        laplace_smoothing_alpha = self.config.base.log_odds_laplace_smoothing_alpha

        population_odds = (
            log_odds[self.p_target_value].sum() + laplace_smoothing_alpha
        ) / (log_odds[self.n_target_value].sum() + laplace_smoothing_alpha)

        # odds of groups
        _odds_col_name = "odds"
        log_odds[_odds_col_name] = (
            log_odds[self.p_target_value] + laplace_smoothing_alpha
        ) / (log_odds[self.n_target_value] + laplace_smoothing_alpha)

        # odds ratio
        _odds_ratio_col_name = "odds_ratio"
        log_odds[_odds_ratio_col_name] = log_odds[_odds_col_name] / population_odds

        # log odds ratio
        log_odds[self.log_odds_col_name] = np.log2(log_odds[_odds_ratio_col_name])
        log_odds[self.log_odds_col_name] = log_odds[self.log_odds_col_name].round(2)

        # replace all special values with 0
        log_odds.fillna(0, inplace=True)
        log_odds.replace([np.inf, -np.inf], 0, inplace=True)

        # add text position for log2odds
        log_odds[self.log_odds_text_col] = "left"
        log_odds.loc[
            log_odds[self.log_odds_col_name] < 0, self.log_odds_text_col
        ] = "right"
        self.__log_odds = log_odds

    def _check_columns(self, df: pd.DataFrame):
        """Checks if df contains all columns (data_col, target_col, count_col)."""
        if self.data_col_name not in df:
            raise ValueError(
                "Data column '{}' not in DataFrame.".format(self.data_col_name)
            )
        if self.target_description.name not in df:
            raise ValueError(
                "Target column '{}' not in DataFrame.".format(
                    self.target_description.name
                )
            )
        if self.count_col_name not in df:
            raise ValueError(
                "Count column not in DataFrame. '{}'".format(self.data_col_name)
            )


class TextDescription(VariableDescription):
    """Interface for unsupervised text variable description.
    Extension of VariableDescription.

    Attributes:
        count_col_name (str): Name of column with word counts.
        words_counts (pd.DataFrame):
            Sorted data with words in data_col_name and counts in count_col_name.
    """

    _words_counts: pd.DataFrame

    @property
    def count_col_name(self) -> str:
        """Name of column with absolute count of word."""
        return "count"

    @property
    def words_counts(self) -> pd.DataFrame:
        if not hasattr(self, "_words_counts"):
            self._words_counts = self._get_word_counts()
        return self._words_counts

    @abstractmethod
    def _get_word_counts(self) -> pd.DataFrame:
        """Generate word counts for input series.

        Returns:
            Series with unique words as index and the computed frequency as value.
        """
        pass


class TextDescriptionSupervised(TextDescription, VariableDescriptionSupervised):
    """Interface for supervised text variable description.
    Extension of TextDescription and VariableDescriptionSupervised.

    Attributes:
        positive_col_name (str): Name of column with word count for positive outcome.
        negative_col_name (str): Name of column with word count for negative outcome.
    """

    @property
    def positive_col_name(self) -> str:
        """Name of column with count of word for positive target."""
        return "positive"

    @property
    def negative_col_name(self) -> str:
        """Name of column with count of word for negative target."""
        return "negative"
