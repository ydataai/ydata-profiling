from typing import Optional, Tuple

import numpy as np
import pandas as pd
from pandas_profiling.model.base.plot_description import BasePlotDescription


class CategoricalPlotDescriptionPandas(BasePlotDescription):
    def __init__(
        self, data_col: pd.Series, target_col: Optional[pd.Series], max_cat_to_plot: int
    ) -> None:
        """Prepare data for plotting"""
        super().__init__(data_col, target_col)

        __count_col_name = self.count_col_name
        self._other_placeholder = "other ..."
        self._max_cat_to_plot = max_cat_to_plot

        # we have 2 different columns
        if target_col is not None and self.data_col_name != self.target_col_name:
            # join columns by id
            data = data_col.to_frame().join(target_col, how="inner").astype(str)
            preprocessed = data.groupby(data.columns.to_list()).size().reset_index()
            preprocessed.rename(columns={0: __count_col_name}, inplace=True)
        else:
            preprocessed = data_col.groupby(data_col).size()
            preprocessed = preprocessed.rename(index=__count_col_name).reset_index()

        # sorts plot
        preprocessed.sort_values(by=__count_col_name, inplace=True, ascending=False)

        # limit the number of plotted categories
        # top_n_classes = preprocessed.drop_duplicates(self.data_col_name)[
        #     self.data_col_name
        # ].head(max_cat_to_plot)
        # if top_n_classes.size < preprocessed[self.data_col_name].nunique():
        #     # select rows, that are not in top n classes and group them
        #     other = preprocessed[~preprocessed[self.data_col_name].isin(top_n_classes)]
        #     if target_col is not None and self.data_col_name != self.target_col_name:
        #         other = (
        #             other.groupby(self.target_col_name)[__count_col_name]
        #             .sum()
        #             .reset_index()
        #         )
        #         other[self.data_col_name] = self._other_placeholder
        #     else:
        #         sum = other[__count_col_name].sum()
        #         other = pd.DataFrame(
        #             data={
        #                 __count_col_name: [sum],
        #                 self.data_col_name: [self._other_placeholder],
        #             }
        #         )
        #     # drop all categories, that are not in top_n_categories
        #     preprocessed = preprocessed[
        #         preprocessed[self.data_col_name].isin(top_n_classes)
        #     ]
        #     # merge top n categories and other
        #     preprocessed = pd.concat([preprocessed, other])
        preprocessed = self._limit_count(preprocessed)
        self._set_preprocessed_data(preprocessed)

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

    def _add_labels_location(self):
        pass

    def get_labels_location(self) -> pd.Series:
        _col_name = "labels_location"
        _df = self.preprocessed_plot[self.count_col_name].to_frame()
        _df[_col_name] = "right"
        _df.loc[
            _df[self.count_col_name] < _df[self.count_col_name].max() / 4, _col_name
        ] = "left"
        return _df[_col_name]


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
            preprocessed_plot = pd.DataFrame()
            for target_value in target_col.unique():
                tmp = get_hist(data_col[target_col == target_value])
                tmp[self.target_col_name] = target_value
                preprocessed_plot = pd.concat([preprocessed_plot, tmp])
        else:
            preprocessed_plot = get_hist(data_col)

        preprocessed_plot.sort_values(
            by=__count_col_name, ascending=False, inplace=True
        )
        self._set_preprocessed_data(preprocessed_plot)
