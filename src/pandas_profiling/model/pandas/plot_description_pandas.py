from typing import Optional

import numpy as np
import pandas as pd
from pandas_profiling.model.base.plot_description import BasePlotDescription


class CategoricalPlotDescriptionPandas(BasePlotDescription):
    def __init__(
        self, data_col: pd.Series, target_col: Optional[pd.Series], max_cat_to_plot: int
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
        super().__init__(data_col, target_col)

        self._other_placeholder = "other ..."
        self._max_cat_to_plot = max_cat_to_plot

        # we have 2 different columns
        if target_col is not None and self.data_col_name != self.target_col_name:
            # join columns by id
            data = data_col.to_frame().join(target_col, how="inner").astype(str)
            distribution = data.groupby(data.columns.to_list()).size().reset_index()
            distribution.rename(columns={0: self.count_col_name}, inplace=True)
        else:
            distribution = data_col.groupby(data_col).size()
            distribution = distribution.rename(index=self.count_col_name).reset_index()

        # sorts plot
        distribution.sort_values(by=self.count_col_name, inplace=True, ascending=False)

        # limit the count of plotted categories
        distribution = self._limit_count(distribution)

        # add column for label position
        distribution = self._add_labels_location(distribution)
        self._validate(distribution)

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
            if (
                self.target_col_name is not None
                and self.data_col_name != self.target_col_name
            ):
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

    def _add_labels_location(self, df: pd.DataFrame):
        col_name = "labels_location"
        df[col_name] = "right"
        df.loc[
            df[self.count_col_name] < df[self.count_col_name].max() / 4, col_name
        ] = "left"
        return df


class NumericPlotDescriptionPandas(BasePlotDescription):
    def __init__(
        self, data_col: pd.Series, target_col: Optional[pd.Series], max_bar_count: int
    ) -> None:
        super().__init__(data_col, target_col)

        def get_hist(col: pd.Series) -> pd.DataFrame:
            """Returns DataFrame with 2 columns (bin_center, count)"""
            hist, bin_edges = np.histogram(col, range=my_range, bins=max_bar_count)
            bin_centers = [
                (bin_edges[i] + bin_edges[i + 1]) / 2 for i in range(len(bin_edges) - 1)
            ]
            return pd.DataFrame(
                data={self.data_col_name: bin_centers, __count_col_name: hist}
            )

        __count_col_name = self.count_col_name
        my_range = (data_col.min(), data_col.max())
        max_bar_count = min(max_bar_count, data_col.nunique())
        # we have target column and one different column
        if target_col is not None and self.data_col_name != self.target_col_name:
            distribution = pd.DataFrame()
            for target_value in target_col.unique():
                tmp = get_hist(data_col[target_col == target_value])
                tmp[self.target_col_name] = target_value
                distribution = pd.concat([distribution, tmp])
        else:
            distribution = get_hist(data_col)

        distribution.sort_values(by=__count_col_name, ascending=False, inplace=True)
        self._validate(distribution)
