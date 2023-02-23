from typing import List, Optional, Tuple

import numpy as np
import pandas as pd
from pandas_profiling.model.description_plot import BasePlotDescription


def get_unique_values(series: pd.Series) -> List[str]:
    arr = series.astype(str).dropna().unique()
    return list(arr)


def get_target_values(
    column: pd.Series, positive: Optional[str] = None
) -> Tuple[str, str]:
    """Return positive target value and negative target value."""
    nunique = column.nunique()
    if nunique != 2:
        raise ValueError(
            "In target should be just 2 unique values. {} were found.".format(nunique)
        )

    if positive is not None:
        unique_values = get_unique_values(column)
        unique_values.remove(str(positive))
        negative_value = unique_values.pop()
        return str(positive), negative_value

    unique_values = get_unique_values(column)
    for unique_value in unique_values:
        # if value is positive value
        if unique_value.casefold() in ["true", "1", "ok"]:
            return get_target_values(column, unique_value)

    # unable to infer
    return unique_values[0], unique_values[1]


class PlotDescriptionPandas(BasePlotDescription):
    """Base class for pandas plot description."""

    _data_col: pd.Series
    _target_col: Optional[pd.Series] = None

    def __init__(
        self,
        data_col: pd.Series,
        target_col: Optional[pd.Series],
        positive_target_value: Optional[str],
    ) -> None:
        self._data_col = data_col
        data_col_name = self.__prepare_data_col_name(data_col)
        target_col_name = self.__prepare_target_col_name(target_col)

        if target_col is not None:
            self._target_col = target_col.astype(str)

            positive, negative = get_target_values(
                self._target_col, positive_target_value
            )
        else:
            positive, negative = None, None
        super().__init__(data_col_name, target_col_name, positive, negative)

    @classmethod
    def __prepare_data_col_name(cls, data_col: pd.Series) -> str:
        """Fills col name, if None.

        Returns column name
        """
        if data_col.name is None:
            data_col.name = "data_col"
        return str(data_col.name)

    @classmethod
    def __prepare_target_col_name(
        cls, target_col: Optional[pd.Series]
    ) -> Optional[str]:
        if target_col is None:
            return None
        if target_col.name is None:
            target_col.name = "target_col"
        return str(target_col.name)


class CategoricalPlotDescriptionPandas(PlotDescriptionPandas):
    _other_placeholder: str = "other ..."
    _max_cat_to_plot: int

    def __init__(
        self,
        data_col: pd.Series,
        target_col: Optional[pd.Series],
        positive_target_value: Optional[str],
        max_cat_to_plot: int,
    ) -> None:
        """Prepare categorical data for plotting

        Parameters
        ----------
        data_col : pd.Series
            series with data, from processed column
        target_col : pd.Series or None
            series with target column, if is set, else None
        max_cat_to_plot : int
            limit for plotting. If we have more categories, than max_cat_to_plot,
            all below threshold will be merged to other category
        """
        data_col = data_col.astype(str)
        super().__init__(data_col, target_col, positive_target_value)

        self._max_cat_to_plot = max_cat_to_plot
        distribution = self._get_distribution()
        self._set_distribution(distribution)

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
            if self.is_supervised():
                other = (
                    other.groupby(self.target_col_name)[self.count_col_name]
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

    def _get_distribution(self) -> pd.DataFrame:
        """Generate grouped distribution DataFrame.
        Limit count of showed categories. Other are merged and showed as last.

        Returns
        -------
        distribution : pd.DataFrame
            Sorted DataFrame with aggregated categories.
        """
        # we have 2 different columns
        if self.is_supervised():
            # join columns by id
            data = (
                self._data_col.to_frame()
                .join(self._target_col, how="inner")
                .astype(str)
            )
            distribution = data.groupby(data.columns.to_list()).size()
            # add zero values
            distribution = distribution.unstack(fill_value=0).stack().reset_index()
            distribution.rename(columns={0: self.count_col_name}, inplace=True)
        else:
            distribution = self._data_col.groupby(self._data_col).size()
            distribution = distribution.reset_index(name=self.count_col_name)

        # sorts plot
        distribution.sort_values(by=self.count_col_name, inplace=True, ascending=False)

        # limit the count of categories
        distribution = self._limit_count(distribution)

        # add column for label position
        distribution = self._add_labels_location(distribution)
        return distribution

    def _add_labels_location(self, df: pd.DataFrame):
        col_name = "labels_location"
        df[col_name] = "right"
        df.loc[
            df[self.count_col_name] < df[self.count_col_name].max() / 4, col_name
        ] = "left"
        return df


class NumericPlotDescriptionPandas(PlotDescriptionPandas):
    """Plot description for numeric columns."""

    def __init__(
        self,
        data_col: pd.Series,
        target_col: Optional[pd.Series],
        positive_target_value: Optional[str],
        bar_count: int,
    ) -> None:
        super().__init__(data_col, target_col, positive_target_value)
        self._bars = bar_count

        distribution = self._get_distribution()
        self._set_distribution(distribution)

    def _get_distribution(self) -> pd.DataFrame:
        """Cut continuous variable to bins.
        For supervised, data_col set to range '[10, 20]'.
        For unsupervised, data_col set to mid of range '15'.

        Returns
        -------
        data : pd.DataFrame
            Binned and grouped data.
        """

        def get_supervised(data: pd.DataFrame) -> pd.DataFrame:
            """Group supervised numeric value.

            Parameters
            ----------
            data : pd.DataFrame
                DataFrame with binned data_col and count_col with zeroes.

            Returns
            -------
            data : pd.DataFrame
                Grouped DataFrame by target_col and data_col.
                Column count_col contains counts for every target data combination.
                Even zero values.
            """
            data = data.join(self._target_col, how="left")
            sub = [self.data_col_name, self.target_col_name]
            # aggregate bins
            data_series = data.groupby(sub)[self.count_col_name].size()
            # add zero values
            data = data_series.unstack(fill_value=0).stack().reset_index()
            data.rename(columns={0: self.count_col_name}, inplace=True)
            data[self.data_col_name] = data[self.data_col_name].astype(str)
            return data

        def get_unsupervised(data: pd.DataFrame) -> pd.DataFrame:
            # replace bins with middle value (10, 20] -> 15
            data[self.data_col_name] = data[self.data_col_name].apply(lambda x: x.mid)
            data[self.data_col_name] = data[self.data_col_name].astype(float)
            sub = [self.data_col_name]
            # aggregate bins
            data_series = data.groupby(sub)[self.count_col_name].size()
            data = data_series.reset_index(name=self.count_col_name)
            return data

        # join columns by id
        data = pd.DataFrame()
        # set precision for col
        # range > 100 -> precision = 1
        # range < 100 -> precision = 2
        # range < 10 -> precision = 3
        range = self._data_col.max() - self._data_col.min()
        if range < 10:
            precision = 3
        elif range < 100:
            precision = 2
        else:
            precision = 1
        # add bins to data_col
        data[self.data_col_name] = pd.cut(
            self._data_col, bins=self._bars, precision=precision
        )
        data[self.count_col_name] = 0
        # group data
        if self.is_supervised():
            data = get_supervised(data)
        else:
            data = get_unsupervised(data)
        return data
