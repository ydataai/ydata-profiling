from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Optional

import numpy as np
import pandas as pd

from pandas_profiling.config import Univariate
from pandas_profiling.model.description_target import TargetDescription


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

    log_odds_col_name: str = "log_odds_ratio"
    _odds_col_name = "odds"
    _odds_ratio_col_name = "odds_ratio"

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

    @abstractmethod
    def get_dist_pivot_table(self) -> pd.DataFrame:
        """Method to get distribution pivot table in following format:

        | col_name  | p_target_value  | n_target_value |
        | --------- | --------------- | -------------- |
        | 1         | 5               | 10             |
        | 2         | 0               | 8              |
        """

    def _generate_odds_ratio(self):
        """Generate odds ratio from distribution pivot table.
        Apply Beta smoothing with alpha + beta is defined from setting
        and alpha/(alpha + beta) = prior.
        - add alpha new records to every group in data
        - distribution of new records is same as distribution in whole population
        - create odds for every group with beta smoothing
        """
        log_odds = self.get_dist_pivot_table()
        # beta smoothing alpha + beta
        imaginary_observations_count = self.config.base.smoothing_parameter

        # get distribution of added records P(positive) + P(negative) = 1
        # P(pos) = sum(positive) / sum(all)
        pos_prob = (log_odds[self.p_target_value].sum()) / (
            log_odds[self.p_target_value].sum() + log_odds[self.n_target_value].sum()
        )
        neg_prob = 1 - pos_prob

        # odds of groups with smoothing
        log_odds[self._odds_col_name] = (
            log_odds[self.p_target_value] + pos_prob * imaginary_observations_count
        ) / (log_odds[self.n_target_value] + neg_prob * imaginary_observations_count)

        # beta smoothing to whole population
        groups = log_odds.shape[0]
        population_odds = (
            log_odds[self.p_target_value].sum()
            + groups * pos_prob * imaginary_observations_count
        ) / (
            log_odds[self.n_target_value].sum()
            + groups * neg_prob * imaginary_observations_count
        )

        # odds ratio = group odds / population odds
        log_odds[self._odds_ratio_col_name] = (
            log_odds[self._odds_col_name] / population_odds
        )
        return log_odds

    def _get_log_odds_ratio(self) -> pd.DataFrame:
        """Generates log2 odds ratio preprocessed DataFrame based on distribution.
        Compute odds for whole population and for every category.
        From that compute log odds ratio.
        """
        log_odds = self._generate_odds_ratio()
        # log odds ratio
        log_odds[self.log_odds_col_name] = np.log2(log_odds[self._odds_ratio_col_name])
        log_odds[self.log_odds_col_name] = log_odds[self.log_odds_col_name].round(2)

        # replace all special values with 0
        log_odds.fillna(0, inplace=True)
        log_odds.replace([np.inf, -np.inf], 0, inplace=True)
        return log_odds


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

    __log_odds: Optional[pd.DataFrame] = None

    @property
    def log_odds(self) -> pd.DataFrame:
        """Returns DataFrame with relative log2odds for data column.
        format:
        | col_name | log_odds |
        | -------- | -------- |
        | male     | -2       |
        | female   | 2        |
        """
        if self.__log_odds is None:
            self.__log_odds = self._get_log_odds_ratio()
        return self.__log_odds

    @property
    @abstractmethod
    def p_value_of_independence(self) -> float:
        """P value of independence between subpopulations.
        For numeric variables:
            p value of student t-test to compare means.
        For categorical values:
            p value of chi square independence test.

        H0: There is no difference.
        """

    def get_dist_pivot_table(self) -> pd.DataFrame:
        """Generate pivot table from distribution.
        transforms distribution:

        | col_name  | target_name  | count |
        | --------- | ------------ | ----- |
        | 1         | 0            | 10    |
        | 1         | 1            | 5     |
        | 2         | 0            | 8     |
        | 2         | 1            | 0     |


        to distribution pivot table:

        | col_name | p_target_value | n_target_value |
        | -------- | -------------- | -------------- |
        | 1        | 5              | 10             |
        | 2        | 0              | 8              |

            - data_col_name is column with data categories
            - p_target_value is count of positive values
            - n_target_value is count of negative values for category

        Returns:
            pd.DataFrame: Distribution as pivot table.
        """
        dist_pivot_table = pd.pivot_table(
            self.distribution,
            values=self.count_col_name,
            index=self.data_col_name,
            columns=self.target_col_name,
            sort=False,
            aggfunc=np.sum,
        ).reset_index()
        dist_pivot_table.columns.name = ""

        # there is possibility, that positive, or negative values will not be present
        if not self.p_target_value in dist_pivot_table:
            dist_pivot_table[self.p_target_value] = 0
        if not self.n_target_value in dist_pivot_table:
            dist_pivot_table[self.n_target_value] = 0
        return dist_pivot_table

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
            DataFrame with one column.
            unique words as index and count_col with computed frequency as value.
        """


class TextDescriptionSupervised(TextDescription, VariableDescriptionSupervised):
    """Interface for supervised text variable description.
    Extension of TextDescription and VariableDescriptionSupervised.

    Attributes:
        positive_col_name (str): Name of column with word count for positive outcome.
        negative_col_name (str): Name of column with word count for negative outcome.
    """

    __log_odds: Optional[pd.DataFrame] = None

    @property
    def log_odds(self) -> pd.DataFrame:
        """Returns DataFrame with relative log2odds for data column.
        format:
        | col_name | log_odds |
        | -------- | -------- |
        | male     | -2       |
        | female   | 2        |
        """
        if self.__log_odds is None:
            self.__log_odds = self._get_log_odds_ratio()
            self.__log_odds = self.__log_odds.sort_values(
                by=self.log_odds_col_name, ascending=False
            )
        return self.__log_odds

    @abstractmethod
    def _get_word_counts(self) -> pd.DataFrame:
        """Generate word counts for input series and target.

        Returns:
            DataFrame with two columns.
            unique words as index and count_col with computed frequency as value.
        """

    def get_dist_pivot_table(self) -> pd.DataFrame:
        return self.words_counts
