import string
from typing import List

import pandas as pd
from pandas_profiling.config import Univariate
from pandas_profiling.model.description_variable import (
    CatDescription,
    CatDescriptionSupervised,
    TextDescription,
    TextDescriptionSupervised,
    VariableDescription,
    VariableDescriptionSupervised,
)
from pandas_profiling.model.pandas.description_target_pandas import (
    TargetDescriptionPandas,
)


class VariableDescriptionPandas(VariableDescription):
    """Base class for pandas unsupervised description.
    Implementation of VariableDescription.
    """

    _config: Univariate
    _data_col_name: str
    _data_col: pd.Series

    def __init__(self, config: Univariate, data_col: pd.Series) -> None:
        self._config = config
        self._data_col_name = self._prepare_data_col_name(data_col)
        self._data_col = data_col

    @property
    def config(self) -> Univariate:
        return self._config

    @property
    def data_col(self) -> pd.Series:
        return self._data_col

    @property
    def data_col_name(self) -> str:
        return self._data_col_name

    @staticmethod
    def _prepare_data_col_name(data_col: pd.Series) -> str:
        """Fills col name, if None.

        Returns column name
        """
        if data_col.name is None:
            data_col.name = "data_col"
        return str(data_col.name)

    @staticmethod
    def _prepare_word_counts(data: pd.Series, stop_words: List[str]) -> pd.Series:
        """Count the number of occurrences of each individual word across
        all lines of the data Series, then sort from the word with the most
        occurrences to the word with the least occurrences. If a list of
        stop words is given, they will be ignored.

        Args:
            data: Series with data, we want to processed.

        Returns:
            Series with unique words as index and the computed frequency as value.
        """
        # get count of values
        value_counts = data.value_counts(dropna=True)
        series = pd.Series(value_counts.index, index=value_counts)
        word_lists = series.str.lower().str.split()
        words = word_lists.explode().str.strip(string.punctuation + string.whitespace)
        word_counts = pd.Series(words.index, index=words)
        # fix for pandas 1.0.5
        word_counts = word_counts[word_counts.index.notnull()]
        word_counts = word_counts.groupby(level=0, sort=False).sum()
        word_counts = word_counts.sort_values(ascending=False)

        # Remove stop words
        if len(stop_words) > 0:
            stop_words = [x.lower() for x in stop_words]
            word_counts = word_counts.loc[~word_counts.index.isin(stop_words)]
        return word_counts


class VariableDescriptionSupervisedPandas(
    VariableDescriptionPandas, VariableDescriptionSupervised
):
    """Base class for pandas plot description.
    Implementation of VariableDescriptionSupervised.
    """

    _target_description: TargetDescriptionPandas

    def __init__(
        self,
        config: Univariate,
        data_col: pd.Series,
        target_description: TargetDescriptionPandas,
    ) -> None:
        self._target_description = target_description
        super().__init__(config=config, data_col=data_col)

    @property
    def target_description(self) -> TargetDescriptionPandas:
        return self._target_description


class CatDescriptionPandas(VariableDescriptionPandas, CatDescription):
    """Class for unsupervised categorical pandas variable description.
    Implementation of CatDescription.
    """

    _other_placeholder: str = "other ..."
    _max_cat_to_plot: int

    def __init__(self, config: Univariate, data_col: pd.Series) -> None:
        """Prepare categorical data for plotting

        Args:
            config (Univariate): Config of variables from report setting.
            data_col (pd.Series): Series with data, from processed column.
        """
        data_col = data_col.astype(str)
        super().__init__(config=config, data_col=data_col)
        self._max_cat_to_plot = self.config.cat.n_obs
        self.distribution

    def _limit_count(self, df: pd.DataFrame) -> pd.DataFrame:
        """Limit count of displayed categories to max_cat.
        All other categories groups to one category 'other'.

        Args:
            df (pd.DataFrame): Categories with counts, we would like to limit size of.
        """
        top_n_classes = df.drop_duplicates(self.data_col_name)[self.data_col_name].head(
            self._max_cat_to_plot
        )
        if top_n_classes.size < df[self.data_col_name].nunique():
            # select rows, that are not in top n classes and group them
            other = df[~df[self.data_col_name].isin(top_n_classes)]

            sum = other[self.count_col_name].sum()
            other = pd.DataFrame(
                data={
                    self.count_col_name: [sum],
                    self.data_col_name: [self._other_placeholder],
                }
            )
            # drop all categories, that are not in top_n_categories
            df = df[df[self.data_col_name].isin(top_n_classes)]
            # merge top n categories and other
            df = pd.concat([df, other])
        return df

    def _generate_distribution(self) -> pd.DataFrame:
        """Generate grouped distribution DataFrame.
        Limit count of showed categories. Other are merged and showed as last.

        Returns:
            distribution (pd.DataFrame): Sorted DataFrame with aggregated categories.
        """

        distribution = self.data_col.groupby(self.data_col).size()
        distribution = distribution.reset_index(name=self.count_col_name)
        # sorts plot
        distribution.sort_values(by=self.count_col_name, inplace=True, ascending=False)
        # limit the count of categories
        distribution = self._limit_count(distribution)
        return distribution


class CatDescriptionSupervisedPandas(
    VariableDescriptionSupervisedPandas, CatDescriptionSupervised
):
    """Class for supervised categorical pandas variable description.
    Implementation of CatDescriptionSupervised
    """

    _other_placeholder: str = "other ..."
    _max_cat_to_plot: int

    def __init__(
        self,
        config: Univariate,
        data_col: pd.Series,
        target_description: TargetDescriptionPandas,
    ) -> None:
        """Describe categorical data.

        Args:
            config (Univariate): Config of variables from report setting.
            data_col (pd.Series): Series with data, from processed column.
            target_description (TargetDescriptionPandas): Description of target series.
        """
        data_col = data_col.astype(str)
        super().__init__(
            config=config, data_col=data_col, target_description=target_description
        )
        self._max_cat_to_plot = self.config.cat.n_obs
        self.log_odds

    def _limit_count(self, df: pd.DataFrame) -> pd.DataFrame:
        """Limit count of displayed categories to max_cat.
        All other categories groups to one category 'other'
        """
        top_n_classes = df.drop_duplicates(self.data_col_name)[self.data_col_name].head(
            self._max_cat_to_plot
        )
        if top_n_classes.size < df[self.data_col_name].nunique():
            # select rows, that are not in top n classes and group them
            other = df[~df[self.data_col_name].isin(top_n_classes)]
            if self.data_col_name != self.target_col_name:
                other = (
                    other.groupby(self.target_description.name)[self.count_col_name]
                    .sum()
                    .reset_index()
                )
                other[self.data_col_name] = self._other_placeholder
            else:
                sum = other[self.count_col_name].sum()
                other = pd.DataFrame(
                    data={
                        self.count_col_name: [sum],
                        self.data_col_name: [self._other_placeholder],
                    }
                )
            # drop all categories, that are not in top_n_categories
            df = df[df[self.data_col_name].isin(top_n_classes)]
            # merge top n categories and other
            df = pd.concat([df, other])
        return df

    def _generate_distribution(self) -> pd.DataFrame:
        """Generate grouped distribution DataFrame.
        Limit count of showed categories. Other are merged and showed as last.

        Returns:
            distribution (pd.DataFrame): Sorted DataFrame with aggregated categories.
        """
        # we have 2 different columns
        if self.data_col_name != self.target_col_name:
            # join columns by id
            data = self.data_col.to_frame().join(
                self.target_description.series_binary, how="inner"
            )
            distribution = data.groupby(data.columns.to_list()).size()
            # add zero values
            distribution = distribution.unstack(fill_value=0).stack().reset_index()
            distribution.rename(columns={0: self.count_col_name}, inplace=True)
        else:
            distribution = self.data_col.groupby(self.data_col).size()
            distribution = distribution.reset_index(name=self.count_col_name)

        # sorts plot
        distribution.sort_values(by=self.count_col_name, inplace=True, ascending=False)

        # limit the count of categories
        distribution = self._limit_count(distribution)
        return distribution


class NumDescriptionPandas(VariableDescriptionPandas, CatDescription):
    """Class for unsupervised numeric pandas variable description.
    Implementation of CatDescription.
    """

    _bars: int

    def __init__(self, config: Univariate, data_col: pd.Series, bar_count: int) -> None:
        """Describe numerical data.

        Args:
            config (Univariate): Config of variables from report setting.
            data_col (pd.Series): Series with data, from processed column.
            bar_count (int): Count of bars for distribution plot.
        """
        self._bars = bar_count
        super().__init__(config=config, data_col=data_col)
        self.distribution

    def _group_distribution(self, data: pd.DataFrame) -> pd.DataFrame:
        """Get unsupervised distribution."""
        # replace bins with middle value (10, 20] -> 15
        data[self.data_col_name] = data[self.data_col_name].apply(lambda x: x.mid)
        data[self.data_col_name] = data[self.data_col_name].astype(float)
        sub = [self.data_col_name]
        # aggregate bins
        data_series = data.groupby(sub)[self.count_col_name].size()
        data = data_series.reset_index(name=self.count_col_name)
        return data

    def _generate_distribution(self) -> pd.DataFrame:
        """Cut continuous variable to bins.
        data_col is set to mid of generated cut.

        Returns:
            data (pd.DataFrame): Binned and grouped data.
        """

        # join columns by id
        data = pd.DataFrame()
        # TODO probably delete
        # set precision for col
        # range > 100 -> precision = 1
        # range < 100 -> precision = 2
        # range < 10 -> precision = 3
        range = self.data_col.max() - self.data_col.min()
        if range < 10:
            precision = 3
        elif range < 100:
            precision = 2
        else:
            precision = 1
        # add bins to data_col
        data[self.data_col_name] = pd.cut(
            self.data_col, bins=self._bars, precision=precision
        )
        data[self.count_col_name] = 0
        # group data
        data = self._group_distribution(data)
        return data


class NumDescriptionSupervisedPandas(
    VariableDescriptionSupervisedPandas, CatDescriptionSupervised
):
    """Class for supervised numeric pandas variable description.
    Implementation of CatDescriptionSupervised.
    """

    _bars: int

    def __init__(
        self,
        config: Univariate,
        data_col: pd.Series,
        bar_count: int,
        target_description: TargetDescriptionPandas,
    ) -> None:
        """Describe numerical supervised data.

        Args:
            config (Univariate): Config of variables from report setting.
            data_col (pd.Series): Series with data, from processed column.
            bar_count (int): Count of bars for distribution plot.
            target_description (TargetDescriptionPandas): Description of target series.
        """
        self._bars = bar_count
        super().__init__(
            config=config,
            data_col=data_col,
            target_description=target_description,
        )
        self.log_odds

    def _generate_distribution(self) -> pd.DataFrame:
        """Cut continuous variable to bins.
        data_col is set to mid of generated cut.

        Returns:
            data (pd.DataFrame): Binned and grouped data.
        """

        # join columns by id
        data = pd.DataFrame()
        # TODO probably delete
        # set precision for col
        # range > 100 -> precision = 1
        # range < 100 -> precision = 2
        # range < 10 -> precision = 3
        range = self.data_col.max() - self.data_col.min()
        if range < 10:
            precision = 3
        elif range < 100:
            precision = 2
        else:
            precision = 1
        # add bins to data_col
        data[self.data_col_name] = pd.cut(
            self.data_col, bins=self._bars, precision=precision
        )
        data[self.count_col_name] = 0
        # group data
        data = self._group_distribution(data)
        return data

    def _group_distribution(self, data: pd.DataFrame) -> pd.DataFrame:
        """Group supervised numeric value.

        Args:
            data (pd.DataFrame): DataFrame with binned data_col
                and count_col with zeroes.

        Returns:
            data (pd.DataFrame):
                Grouped DataFrame by target_col and data_col.
                Column count_col contains counts for every target data combination.
                Even zero values.
        """
        data = data.join(self.target_description.series_binary, how="left")
        sub = [self.data_col_name, self.target_description.name]
        # aggregate bins
        data_series = data.groupby(sub)[self.count_col_name].size()
        # add zero values
        data = data_series.unstack(fill_value=0).stack().reset_index()
        data.rename(columns={0: self.count_col_name}, inplace=True)
        data[self.data_col_name] = data[self.data_col_name].astype(str)
        return data


class TextDescriptionPandas(VariableDescriptionPandas, TextDescription):
    """Class for unsupervised text pandas variable description.
    Implementation of TextDescription.
    """

    stop_words: List[str] = []

    def __init__(self, config: Univariate, data_col: pd.Series) -> None:
        """Describe text unsupervised data.

        Args:
            config (Univariate): Config of variables from report setting.
            data_col (pd.Series): Series with data, from processed column.
        """
        super().__init__(config=config, data_col=data_col)
        self.stop_words = self.config.cat.stop_words
        self.words_counts

    def _get_word_counts(self) -> pd.DataFrame:
        return self._prepare_word_counts(self.data_col, self.stop_words).to_frame(
            name=self.count_col_name
        )


class TextDescriptionSupervisedPandas(
    VariableDescriptionSupervisedPandas, TextDescriptionSupervised
):
    stop_words: List[str] = []

    def __init__(
        self,
        config: Univariate,
        data_col: pd.Series,
        target_description: TargetDescriptionPandas,
    ) -> None:
        """Describe text supervised data.

        Args:
            config (Univariate): Config of variables from report setting.
            data_col (pd.Series): Series with data, from processed column.
            target_description (TargetDescriptionPandas): Description of target series.
        """
        super().__init__(
            config=config,
            data_col=data_col,
            target_description=target_description,
        )
        self.stop_words = self.config.cat.stop_words
        self.words_counts

    def _get_word_counts_supervised(self) -> pd.DataFrame:
        if not self.target_description:
            raise ValueError("target not found in {}".format(self.data_col_name))
        # join data and target col
        data = self.data_col.to_frame().join(self.target_description.series_binary)
        # split data col by target to positive and negative
        positive_vals = data.loc[
            data[self.target_description.name] == self.target_description.bin_positive,
            self.data_col_name,
        ]
        negative_vals = data.loc[
            data[self.target_description.name] == self.target_description.bin_negative,
            self.data_col_name,
        ]
        positive_counts = self._prepare_word_counts(
            positive_vals, self.stop_words
        ).to_frame(name=self.p_target_value)
        negative_counts = self._prepare_word_counts(
            negative_vals, self.stop_words
        ).to_frame(name=self.n_target_value)
        # join positive and negative word counts
        word_counts = positive_counts.join(negative_counts, how="outer")
        word_counts.fillna(0, inplace=True)
        word_counts[self.p_target_value] = word_counts[self.p_target_value].astype(int)
        word_counts[self.n_target_value] = word_counts[self.n_target_value].astype(int)
        word_counts[self.count_col_name] = (
            word_counts[self.p_target_value] + word_counts[self.n_target_value]
        )
        return word_counts.sort_values(by=self.count_col_name, ascending=False)

    def _get_word_counts(self) -> pd.DataFrame:
        return self._get_word_counts_supervised()
