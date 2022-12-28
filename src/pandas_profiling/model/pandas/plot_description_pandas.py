from typing import Optional
import pandas as pd

from pandas_profiling.model.base.plot_description import BasePlotDescription


class CategoricalPlotDescriptionPandas(BasePlotDescription):
    def __init__(
        self, data_col: pd.Series, target_col: Optional[pd.Series], max_cat_to_plot: int
    ) -> None:
        """Prepare data for plotting"""
        __count_col_name = "count"
        __other_placeholder = "other ..."
        if data_col.name is None:
            data_col.name = "data_col"

        data_col_name = str(data_col.name)
        target_col_name = None
        # we have 2 different columns
        if target_col is not None and data_col_name != target_col.name:
            target_col_name = str(target_col.name)
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
        preprocessed.reset_index(inplace=True, drop=True)
        super().__init__(preprocessed, data_col_name, target_col_name)
