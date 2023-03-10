from math import log2
from typing import Any

import numpy as np
import pandas as pd
import pytest
from pandas_profiling.config import Settings, Univariate
from pandas_profiling.model.description_variable import CatDescriptionSupervised
from pandas_profiling.model.pandas.description_target_pandas import (
    TargetDescription,
    TargetDescriptionPandas,
)


class MockCatDescription(CatDescriptionSupervised):
    _config: Settings
    _dist: pd.DataFrame
    _target_desc: TargetDescriptionPandas

    def __init__(self, dist: pd.DataFrame, laplace_alpha: int):
        self._config = Settings()
        self._config.target.col_name = "target"
        self._config.vars.base.log_odds_laplace_smoothing_alpha = laplace_alpha
        self._dist = dist
        self._target_desc = TargetDescriptionPandas(self._config.target, dist["data"])

    @property
    def config(self) -> Univariate:
        return self._config.vars

    @property
    def data_col(self) -> Any:
        return None

    @property
    def data_col_name(self) -> str:
        return "data"

    @property
    def distribution(self) -> pd.DataFrame:
        return self._dist

    @property
    def target_description(self) -> TargetDescription:
        return self._target_desc

    def _generate_distribution(self):
        pass


@pytest.mark.parametrize(
    "distribution, expected_pivot, expected_odds, expected_odds_ratio, expected_log_odds_ratio, laplace_alpha",
    [
        (
            # distribution
            pd.DataFrame(
                [("male", 0, 25), ("male", 1, 15), ("female", 0, 5), ("female", 1, 15)],
                columns=["data", "target", "count"],
            ),
            # expected_pivot
            np.array([("male", 25, 15), ("female", 5, 15)]),
            # expected_odds
            np.array([("male", 0.6), ("female", 3)]),
            # expected_odds_ratio
            np.array([("male", 0.6), ("female", 3)]),
            # expected_log_odds_ratio
            np.array([("male", log2(0.6)), ("female", log2(3))]),
            # laplace_alpha
            0,
        ),
        (
            # distribution
            pd.DataFrame(
                [("male", 0, 5), ("male", 1, 10), ("female", 0, 10), ("female", 1, 5)],
                columns=["data", "target", "count"],
            ),
            # expected_pivot
            np.array([("male", 5, 10), ("female", 10, 5)]),
            # expected_odds
            np.array([("male", 2), ("female", 0.5)]),
            # expected_odds_ratio
            np.array([("male", 2), ("female", 0.5)]),
            # expected_log_odds_ratio
            np.array([("male", 1), ("female", -1)]),
            # laplace_alpha
            0,
        ),
        (
            # distribution
            pd.DataFrame(
                [("male", 0, 25), ("male", 1, 5), ("female", 0, 15), ("female", 1, 15)],
                columns=["data", "target", "count"],
            ),
            # expected_pivot
            np.array([("male", 25, 5), ("female", 15, 15)]),
            # expected_odds
            np.array([("male", 0.2), ("female", 1)]),
            # expected_odds_ratio
            np.array([("male", 0.4), ("female", 2)]),
            # expected_log_odds_ratio
            np.array([("male", log2(0.4)), ("female", log2(2))]),
            # laplace_alpha
            0,
        ),
        (
            # distribution
            pd.DataFrame(
                [("male", 0, 25), ("male", 1, 5), ("female", 0, 15), ("female", 1, 15)],
                columns=["data", "target", "count"],
            ),
            # expected_pivot
            np.array([("male", 25, 5), ("female", 15, 15)]),
            # expected_odds
            np.array([("male", 10 / 35), ("female", 20 / 25)]),
            # expected_odds_ratio
            np.array([("male", (10 / 35) / 0.5), ("female", (20 / 25) / 0.5)]),
            # expected_log_odds_ratio
            np.array(
                [("male", log2((10 / 35) / 0.5)), ("female", log2((20 / 25) / 0.5))]
            ),
            # laplace_alpha
            15,
        ),
    ],
)
class TestCat:
    def test_pivot_table(
        self,
        distribution: pd.DataFrame,
        expected_pivot: np.ndarray,
        expected_odds,
        expected_odds_ratio,
        expected_log_odds_ratio,
        laplace_alpha,
    ):
        desc = MockCatDescription(distribution, laplace_alpha)
        expected_pivot_pd = pd.DataFrame(
            expected_pivot,
            columns=[desc.data_col_name, desc.n_target_value, desc.p_target_value],
        )
        expected_pivot_pd[desc.n_target_value] = expected_pivot_pd[
            desc.n_target_value
        ].astype(int)
        expected_pivot_pd[desc.p_target_value] = expected_pivot_pd[
            desc.p_target_value
        ].astype(int)

        pivot_table = desc._generate_dist_pivot_table()
        assert pivot_table.shape[0] == len(expected_pivot), "Incorrect number of rows."
        assert pivot_table.compare(
            expected_pivot_pd
        ).empty, "Incorrect values in distribution pivot table."

    def test_odds(
        self,
        distribution: pd.DataFrame,
        expected_pivot,
        expected_odds: np.ndarray,
        expected_odds_ratio,
        expected_log_odds_ratio,
        laplace_alpha,
    ):
        desc = MockCatDescription(distribution, laplace_alpha)
        expected_odds_pd = pd.DataFrame(
            expected_odds,
            columns=[desc.data_col_name, desc._odds_col_name],
        )
        expected_odds_pd[desc._odds_col_name] = expected_odds_pd[
            desc._odds_col_name
        ].astype(float)

        odds_ratio = desc._generate_odds_ratio()
        assert (
            odds_ratio[[desc.data_col_name, desc._odds_col_name]]
            .compare(expected_odds_pd)
            .empty
        ), "Incorrect values in odds table."

    def test_odds_ratio(
        self,
        distribution: pd.DataFrame,
        expected_pivot,
        expected_odds,
        expected_odds_ratio: np.ndarray,
        expected_log_odds_ratio,
        laplace_alpha,
    ):
        desc = MockCatDescription(distribution, laplace_alpha)
        expected_odds_ratio_pd = pd.DataFrame(
            expected_odds_ratio,
            columns=[desc.data_col_name, desc._odds_ratio_col_name],
        )
        expected_odds_ratio_pd[desc._odds_ratio_col_name] = expected_odds_ratio_pd[
            desc._odds_ratio_col_name
        ].astype(float)

        odds_ratio = desc._generate_odds_ratio()
        print(odds_ratio)
        print(expected_odds_ratio_pd)
        assert (
            odds_ratio[[desc.data_col_name, desc._odds_ratio_col_name]]
            .compare(expected_odds_ratio_pd)
            .empty
        ), "Incorrect values in odds ratio table."

    def test_log2odds_ratio(
        self,
        distribution: pd.DataFrame,
        expected_pivot,
        expected_odds,
        expected_odds_ratio,
        expected_log_odds_ratio: np.ndarray,
        laplace_alpha,
    ):
        desc = MockCatDescription(distribution, laplace_alpha)
        expected_log_odds_ratio_pd = pd.DataFrame(
            expected_log_odds_ratio,
            columns=[desc.data_col_name, desc.log_odds_col_name],
        )
        expected_log_odds_ratio_pd[desc.log_odds_col_name] = (
            expected_log_odds_ratio_pd[desc.log_odds_col_name].astype(float).round(2)
        )

        log_odds_ratio = desc.log_odds
        print(log_odds_ratio)
        print(expected_log_odds_ratio_pd)
        assert (
            log_odds_ratio[[desc.data_col_name, desc.log_odds_col_name]]
            .compare(expected_log_odds_ratio_pd)
            .empty
        ), "Incorrect values in log odds ratio table."
