from typing import Optional, Tuple

import numpy as np
import pandas as pd
from pandas_profiling.model.base.plot_description import BasePlotDescription


class CategoricalPlotDescriptionPandas(BasePlotDescription):
    def __init__(
        self, data_col: pd.Series, target_col: Optional[pd.Series], max_cat_to_plot: int
    ) -> None:
        """Prepare data for plotting"""
        __count_col_name = self.count_col_name
        __other_placeholder = "other ..."
        data_col_name = self.prepare_data_col(data_col)
        target_col_name = self.prepare_target_col(target_col)

        # we have 2 different columns
        if target_col is not None and data_col_name != target_col_name:
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
        top_n_classes = preprocessed.drop_duplicates(data_col_name)[data_col_name].head(
            max_cat_to_plot
        )
        if top_n_classes.size < preprocessed[data_col_name].nunique():
            # select rows, that are not in top n classes and group them
            other = preprocessed[~preprocessed[data_col_name].isin(top_n_classes)]
            if target_col is not None and data_col_name != target_col_name:
                other = (
                    other.groupby(target_col_name)[__count_col_name].sum().reset_index()
                )
                other[data_col_name] = __other_placeholder
            else:
                sum = other[__count_col_name].sum()
                other = pd.DataFrame(
                    data={__count_col_name: [sum], data_col_name: [__other_placeholder]}
                )
            # drop all categories, that are not in top_n_categories
            preprocessed = preprocessed[preprocessed[data_col_name].isin(top_n_classes)]
            # merge top n categories and other
            preprocessed = pd.concat([preprocessed, other])
        super().__init__(preprocessed, data_col_name, target_col_name)

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
        def get_hist(col: pd.Series) -> pd.DataFrame:
            """Returns DataFrame with 2 columns (bin_center, count)"""
            hist, bin_edges = np.histogram(col, range=my_range, bins=max_bar_count)
            bin_centers = [
                (bin_edges[i] + bin_edges[i + 1]) / 2 for i in range(len(bin_edges) - 1)
            ]
            return pd.DataFrame(
                data={data_col_name: bin_centers, __count_col_name: hist}
            )

        __count_col_name = self.count_col_name
        data_col_name = self.prepare_data_col(data_col)
        target_col_name = self.prepare_target_col(target_col)
        my_range = (data_col.min(), data_col.max())
        max_bar_count = min(max_bar_count, data_col.nunique())
        # we have target column and one different column
        if target_col is not None and data_col_name != target_col_name:
            preprocessed_plot = pd.DataFrame()
            for target_value in target_col.unique():
                tmp = get_hist(data_col[target_col == target_value])
                tmp[target_col_name] = target_value
                preprocessed_plot = pd.concat([preprocessed_plot, tmp])
        else:
            preprocessed_plot = get_hist(data_col)

        preprocessed_plot.sort_values(
            by=__count_col_name, ascending=False, inplace=True
        )

        super().__init__(preprocessed_plot, data_col_name, target_col_name)
