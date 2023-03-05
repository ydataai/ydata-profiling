from typing import Any

import numpy as np
import pandas as pd
import pytest
from pandas_profiling.config import Target, Univariate
from pandas_profiling.model.pandas.description_plot_pandas import (
    BasePlotDescription,
    CategoricalPlotDescriptionPandas,
    CategoricPlotDescription,
    NumericPlotDescriptionPandas,
)
from pandas_profiling.model.pandas.description_target_pandas import (
    TargetDescriptionPandas,
)


def compare_distribution_supervised(
    plot_description: CategoricPlotDescription, expected_dist: pd.DataFrame
):
    assert plot_description.target_col_name, "Target shouldn't be None."
    # check distribution
    dist = plot_description.distribution
    expected_dist["data"] = expected_dist["data"].astype(str)
    expected_dist["target"] = expected_dist["target"].astype(int)
    expected_dist["count"] = expected_dist["count"].astype(int)

    # check types of columns
    assert dist[plot_description.data_col_name].dtype == "object"
    assert dist[plot_description.target_col_name].dtype == "int"
    assert dist[plot_description.count_col_name].dtype == "int"
    # check if all columns are present
    for index, row in expected_dist.iterrows():
        assert (
            (dist[plot_description.data_col_name] == row["data"])
            & (dist[plot_description.target_col_name] == row["target"])
            & (dist[plot_description.count_col_name] == row["count"])
        ).any(), "Row '{}' does not found.".format(row)
    assert dist.shape[0] == expected_dist.shape[0], "Distributions have different size."


@pytest.mark.parametrize(
    "test_data, expected_distribution",
    [
        (
            # lvl, survived
            np.array([(1, 0), (1, 0), (1, 0), (5, 1), (5, 0), (5, 1)]),
            # lvl, survived, count
            np.array([(1, 0, 3), (5, 1, 2), (5, 0, 1), (1, 1, 0)]),
        ),
        (
            # sex, survived
            np.array(
                [("male", 0), ("male", 0), ("male", 1), ("female", 1), ("female", 1)]
            ),
            np.array(
                [("male", 0, 2), ("male", 1, 1), ("female", 0, 0), ("female", 1, 2)]
            ),
        ),
    ],
)
def test_categorical_plot_description(test_data, expected_distribution):
    target_setting = Target()
    target_setting.col_name = "target"
    df = pd.DataFrame.from_records(test_data, columns=["data", "target"])
    target_description = TargetDescriptionPandas(target_setting, df["target"])
    description = CategoricalPlotDescriptionPandas(
        Univariate(), df["data"], target_description, 5
    )
    expected = pd.DataFrame(expected_distribution, columns=["data", "target", "count"])
    compare_distribution_supervised(description, expected)


@pytest.mark.parametrize(
    "test_data, expected_distribution",
    [
        (
            # lvl, survived
            np.array([(1, 0), (1, 0), (1, 0), (5, 1), (5, 0), (5, 1)]),
            # lvl, survived, count
            np.array(
                [
                    ("(0.996, 3.0]", 0, 3),
                    ("(0.996, 3.0]", 1, 0),
                    ("(3.0, 5.0]", 0, 1),
                    ("(3.0, 5.0]", 1, 2),
                ]
            ),
        ),
    ],
)
def test_numeric_plot_description(test_data, expected_distribution):
    target_setting = Target()
    target_setting.col_name = "target"
    df = pd.DataFrame.from_records(test_data, columns=["data", "target"])
    target_description = TargetDescriptionPandas(target_setting, df["target"])
    description = NumericPlotDescriptionPandas(
        Univariate(), df["data"], target_description, 2
    )
    expected = pd.DataFrame(expected_distribution, columns=["data", "target", "count"])
    compare_distribution_supervised(description, expected)
