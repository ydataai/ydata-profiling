import pandas as pd
import numpy as np
import datetime
import pytest

from pandas_profiling import config
from pandas_profiling.model.base import Variable

check_is_NaN = "pandas_profiling.check_is_NaN"

from pandas_profiling.model.describe import describe_1d, describe

testdata = [
    # Unique values
    (pd.Series([1, 2]), True, 1),
    # Unique values including nan
    (pd.Series([np.nan]), None, None),
    # Unique values all nan
    (pd.Series([1, 2, np.nan]), True, 1),
    # Non unique values
    (pd.Series([1, 2, 2]), False, 2 / 3),
    # Non unique nan
    (pd.Series([1, np.nan, np.nan]), True, 1),
    # Non unique values including nan
    (pd.Series([1, 2, 2, np.nan]), False, 2 / 3),
    # Non unique values including non unique nan
    (pd.Series([1, 2, 2, np.nan, np.nan]), False, 2 / 3),
]


@pytest.mark.parametrize("data,is_unique,p_unique", testdata)
def test_describe_unique(data, is_unique, p_unique):
    """Test the unique feature of 1D data"""

    desc_1d = describe_1d(data)
    if is_unique is not None:
        assert desc_1d["p_unique"] == p_unique, "Describe 1D p_unique incorrect"
        assert desc_1d["is_unique"] == is_unique, "Describe 1D should return unique"


@pytest.fixture
def recoding_data():
    data = {
        "x": [
            "chien",
            "chien",
            "chien",
            "chien",
            "chat",
            "chat",
            "chameaux",
            "chameaux",
        ],
        "y": ["dog", "dog", "dog", "dog", "cat", "cat", "camel", "camel"],
    }
    df = pd.DataFrame(data)

    return df


# def test_recoding_reject(recoding_data):
#     config["correlations"]["recoded"]["calculate"] = True
#     config["correlations"]["recoded"]["warn_high_correlations"] = True
#     results = describe(recoding_data)
#
#     assert (
#         results["variables"]["y"]["type"] == Variable.S_TYPE_RECODED
#         and results["variables"]["x"]["type"] == Variable.TYPE_CAT
#     ) or (
#         results["variables"]["x"]["type"] == Variable.S_TYPE_RECODED
#         and results["variables"]["y"]["type"] == Variable.TYPE_CAT
#     ), "Type is wrong"
#     assert (
#         "correlation_var" in results["variables"]["y"]
#         and results["variables"]["y"]["correlation_var"] == "x"
#     ) or (
#         "correlation_var" in results["variables"]["x"]
#         and results["variables"]["x"]["correlation_var"] == "y"
#     ), "Values should be equal"
#
#     expected_results = {
#         "n_cells_missing": 0.0,
#         Variable.S_TYPE_UNIQUE.value: 0,
#         Variable.S_TYPE_CONST.value: 0,
#         "nvar": 2,
#         Variable.S_TYPE_REJECTED.value: 1,
#         "n": 8,
#         Variable.S_TYPE_RECODED.value: 1,
#         Variable.S_TYPE_CORR.value: 0,
#         Variable.TYPE_DATE.value: 0,
#         Variable.TYPE_NUM.value: 0,
#         Variable.TYPE_CAT.value: 1,
#         "n_duplicates": 5,
#     }
#     for key in expected_results:
#         assert (
#             results["table"][key] == expected_results[key]
#         ), "recoding error {}".format(key)
#
#
# def test_cramers_reject(recoding_data):
#     recoding_data.loc[len(recoding_data)] = {"x": "chat", "y": "dog"}
#     config["check_correlation_cramers"] = True
#     config["correlation_threshold_cramers"] = 0.1
#     config["correlations"]["cramers"] = True
#     results = describe(recoding_data)
#
#     # The order of dicts is not preserved in Python 3.5 and not guaranteed in Python 3.6
#     assert (
#         results["variables"]["y"]["type"] == Variable.S_TYPE_CORR
#         and results["variables"]["x"]["type"] == Variable.TYPE_CAT
#     ) or (
#         results["variables"]["x"]["type"] == Variable.S_TYPE_CORR
#         and results["variables"]["y"]["type"] == Variable.TYPE_CAT
#     ), "Type is wrong"
#     assert (
#         "correlation_var" in results["variables"]["y"]
#         and results["variables"]["y"]["correlation_var"] == "x"
#     ) or (
#         "correlation_var" in results["variables"]["x"]
#         and results["variables"]["x"]["correlation_var"] == "y"
#     ), "Values should be equal"
#
#     expected_results = {
#         "n_cells_missing": 0.0,
#         Variable.S_TYPE_UNIQUE.value: 0,
#         Variable.S_TYPE_CONST.value: 0,
#         "nvar": 2,
#         Variable.S_TYPE_REJECTED.value: 1,
#         "n": 9,
#         Variable.S_TYPE_RECODED.value: 0,
#         Variable.S_TYPE_CORR.value: 1,
#         Variable.TYPE_DATE.value: 0,
#         Variable.TYPE_NUM.value: 0,
#         Variable.TYPE_CAT.value: 1,
#         "n_duplicates": 5,
#     }
#     for key in expected_results:
#         assert (
#             results["table"][key] == expected_results[key]
#         ), "recoding error {}".format(key)


@pytest.fixture
def describe_data():
    data = {
        "id": [chr(97 + c) for c in range(1, 9)] + ["d"],
        "x": [50, 50, -10, 0, 0, 5, 15, -3, None],
        "y": [0.000001, 654.152, None, 15.984512, 3122, -3.1415926535, 111, 15.9, 13.5],
        "cat": [
            "a",
            "long text value",
            u"Élysée",
            "",
            None,
            "some <b> B.s </div> </div> HTML stuff",
            "c",
            "c",
            "c",
        ],
        "s1": np.ones(9),
        "s2": [u"some constant text $ % value {obj} " for _ in range(1, 10)],
        "somedate": [
            datetime.date(2011, 7, 4),
            datetime.datetime(2022, 1, 1, 13, 57),
            datetime.datetime(1990, 12, 9),
            np.nan,
            datetime.datetime(1990, 12, 9),
            datetime.datetime(1950, 12, 9),
            datetime.datetime(1898, 1, 2),
            datetime.datetime(1950, 12, 9),
            datetime.datetime(1950, 12, 9),
        ],
        "bool_tf": [True, True, False, True, False, True, True, False, True],
        "bool_tf_with_nan": [
            True,
            False,
            False,
            False,
            False,
            True,
            True,
            False,
            np.nan,
        ],
        "bool_01": [1, 1, 0, 1, 1, 0, 0, 0, 1],
        "bool_01_with_nan": [1, 0, 1, 0, 0, 1, 1, 0, np.nan],
        "list": [
            [1, 2],
            [1, 2],
            [1, 2],
            [1, 2],
            [1, 2],
            [1, 2],
            [1, 2],
            [1, 2],
            [1, 2],
        ],
        "mixed": [1, 2, "a", 4, 5, 6, 7, 8, 9],
        "dict": [
            {"a": "a"},
            {"b": "b"},
            {"c": "c"},
            {"d": "d"},
            {"e": "e"},
            {"f": "f"},
            {"g": "g"},
            {"h": "h"},
            {"i": "i"},
        ],
        "tuple": [
            (1, 2),
            (3, 4),
            (5, 6),
            (7, 8),
            (9, 10),
            (11, 12),
            (13, 14),
            (15, 16),
            (17, 18),
        ],
    }
    return data


@pytest.fixture
def expected_results():
    return {
        "id": {
            "25%": check_is_NaN,
            "5%": check_is_NaN,
            "50%": check_is_NaN,
            "75%": check_is_NaN,
            "95%": check_is_NaN,
            "count": 9,
            "cv": check_is_NaN,
            "distinct_count": 8,
            "freq": 2,
            "histogram": check_is_NaN,
            "iqr": check_is_NaN,
            "is_unique": False,
            "kurtosis": check_is_NaN,
            "mad": check_is_NaN,
            "max": check_is_NaN,
            "mean": check_is_NaN,
            "min": check_is_NaN,
            "mini_histogram": check_is_NaN,
            "n_missing": 0,
            "p_missing": 0.0,
            "p_unique": 0.88888888,
            "p_zeros": check_is_NaN,
            "range": check_is_NaN,
            "skewness": check_is_NaN,
            "std": check_is_NaN,
            "sum": check_is_NaN,
            "top": "d",
            "type": Variable.TYPE_CAT,
            "variance": check_is_NaN,
        },
        "x": {
            "25%": -0.75,
            "5%": -7.5499999999999989,
            "50%": 2.5,
            "75%": 23.75,
            "95%": 50.0,
            "count": 8,
            "n_infinite": 0,
            "p_infinite": 0,
            "cv": 1.771071190261633,
            "distinct_count": 6,
            "freq": check_is_NaN,
            "iqr": 24.5,
            "is_unique": False,
            "kurtosis": -0.50292858929003803,
            "mad": 18.71875,
            "max": 50.0,
            "mean": 13.375,
            "min": -10.0,
            "mode": 0.0,
            "n_missing": 1,
            "p_missing": 0.11111111111111116,
            "p_unique": 6 / 8,
            "p_zeros": 0.2222222222222222,
            "range": 60.0,
            "skewness": 1.0851622393567653,
            "std": 23.688077169749342,
            "sum": 107.0,
            "top": check_is_NaN,
            "type": Variable.TYPE_NUM,
            "variance": 561.125,
        },
        "y": {
            "25%": 10.125000249999999,
            "5%": -2.0420348747749997,
            "50%": 15.942256,
            "75%": 246.78800000000001,
            "95%": 2258.2531999999987,
            "count": 8,
            "n_infinite": 0,
            "p_infinite": 0,
            "cv": 2.2112992878833846,
            "distinct_count": 8,
            "freq": check_is_NaN,
            "iqr": 236.66299975000001,
            "is_unique": True,
            "kurtosis": 6.974137018717359,
            "mad": 698.45081747834365,
            "max": 3122.0,
            "mean": 491.17436504331249,
            "min": -3.1415926535000001,
            "mode": 9.9999999999999995e-07,
            "n_missing": 1,
            "p_missing": 0.11111111111111116,
            "p_unique": 1,
            "p_zeros": 0.0,
            "range": 3125.1415926535001,
            "skewness": 2.6156591135729266,
            "std": 1086.1335236468506,
            "sum": 3929.3949203464999,
            "top": check_is_NaN,
            "type": Variable.TYPE_NUM,
            "variance": 1179686.0311895239,
        },
        "cat": {
            "25%": check_is_NaN,
            "5%": check_is_NaN,
            "50%": check_is_NaN,
            "75%": check_is_NaN,
            "95%": check_is_NaN,
            "count": 8,
            "cv": check_is_NaN,
            "distinct_count": 6,
            "freq": 3,
            "histogram": check_is_NaN,
            "iqr": check_is_NaN,
            "is_unique": False,
            "kurtosis": check_is_NaN,
            "mad": check_is_NaN,
            "max": check_is_NaN,
            "mean": check_is_NaN,
            "min": check_is_NaN,
            "mini_histogram": check_is_NaN,
            "mode": "c",
            "n_missing": 1,
            "p_missing": 0.11111111111111116,
            "p_unique": 6 / 8,
            "p_zeros": check_is_NaN,
            "range": check_is_NaN,
            "skewness": check_is_NaN,
            "std": check_is_NaN,
            "sum": check_is_NaN,
            "top": "c",
            "type": Variable.TYPE_CAT,
            "variance": check_is_NaN,
        },
        "s1": {
            "25%": check_is_NaN,
            "5%": check_is_NaN,
            "50%": check_is_NaN,
            "75%": check_is_NaN,
            "95%": check_is_NaN,
            "count": 9,
            "cv": check_is_NaN,
            "distinct_count": 1,
            "freq": 9,
            "histogram": check_is_NaN,
            "iqr": check_is_NaN,
            "is_unique": False,
            "kurtosis": check_is_NaN,
            "mad": check_is_NaN,
            "max": check_is_NaN,
            "mean": check_is_NaN,
            "min": check_is_NaN,
            "mini_histogram": check_is_NaN,
            "mode": 1.0,
            "n_missing": 0,
            "p_missing": 0.0,
            "p_unique": 0.1111111111111111,
            "p_zeros": check_is_NaN,
            "range": check_is_NaN,
            "skewness": check_is_NaN,
            "std": check_is_NaN,
            "sum": check_is_NaN,
            "top": 1.0,
            "type": Variable.TYPE_BOOL,
            "variance": check_is_NaN,
        },
        "s2": {
            "25%": check_is_NaN,
            "5%": check_is_NaN,
            "50%": check_is_NaN,
            "75%": check_is_NaN,
            "95%": check_is_NaN,
            "count": 9,
            "cv": check_is_NaN,
            "distinct_count": 1,
            "freq": 9,
            "histogram": check_is_NaN,
            "iqr": check_is_NaN,
            "is_unique": False,
            "kurtosis": check_is_NaN,
            "mad": check_is_NaN,
            "max": check_is_NaN,
            "mean": check_is_NaN,
            "min": check_is_NaN,
            "mini_histogram": check_is_NaN,
            "mode": u"some constant text $ % value {obj} ",
            "n_missing": 0,
            "p_missing": 0.0,
            "p_unique": 0.1111111111111111,
            "p_zeros": check_is_NaN,
            "range": check_is_NaN,
            "skewness": check_is_NaN,
            "std": check_is_NaN,
            "sum": check_is_NaN,
            "top": "some constant text $ % value {obj} ",
            "type": Variable.TYPE_CAT,
            "variance": check_is_NaN,
        },
        "somedate": {
            "25%": check_is_NaN,
            "5%": check_is_NaN,
            "50%": check_is_NaN,
            "75%": check_is_NaN,
            "95%": check_is_NaN,
            "count": 8,
            "cv": check_is_NaN,
            "distinct_count": 5,
            "freq": check_is_NaN,
            "iqr": check_is_NaN,
            "is_unique": False,
            "kurtosis": check_is_NaN,
            "mad": check_is_NaN,
            "max": datetime.datetime(2022, 1, 1, 13, 57),
            "mean": check_is_NaN,
            "min": datetime.datetime(1898, 1, 2),
            "mode": datetime.datetime(1950, 12, 9),
            "n_missing": 1,
            "p_missing": 0.11111111111111116,
            "p_unique": 5 / 8,
            "p_zeros": check_is_NaN,
            "range": datetime.timedelta(45289, hours=13, minutes=57),
            "skewness": check_is_NaN,
            "std": check_is_NaN,
            "sum": check_is_NaN,
            "top": check_is_NaN,
            "type": Variable.TYPE_DATE,
        },
        "bool_tf": {
            "25%": check_is_NaN,
            "5%": check_is_NaN,
            "50%": check_is_NaN,
            "75%": check_is_NaN,
            "95%": check_is_NaN,
            "count": 9,
            "cv": check_is_NaN,
            "distinct_count": 2,
            "freq": 6,
            "histogram": check_is_NaN,
            "iqr": check_is_NaN,
            "is_unique": False,
            "kurtosis": check_is_NaN,
            "mad": check_is_NaN,
            "max": check_is_NaN,
            "min": check_is_NaN,
            "mini_histogram": check_is_NaN,
            "mode": True,
            "n_missing": 0,
            "p_missing": 0,
            "p_unique": 2 / 9,
            "p_zeros": check_is_NaN,
            "range": check_is_NaN,
            "skewness": check_is_NaN,
            "std": check_is_NaN,
            "sum": check_is_NaN,
            "top": True,
            "type": Variable.TYPE_BOOL,
            "variance": check_is_NaN,
        },
        "bool_tf_with_nan": {
            "25%": check_is_NaN,
            "5%": check_is_NaN,
            "50%": check_is_NaN,
            "75%": check_is_NaN,
            "95%": check_is_NaN,
            "count": 8,
            "cv": check_is_NaN,
            "distinct_count": 2,
            "freq": 5,
            "histogram": check_is_NaN,
            "iqr": check_is_NaN,
            "is_unique": False,
            "kurtosis": check_is_NaN,
            "mad": check_is_NaN,
            "max": check_is_NaN,
            "min": check_is_NaN,
            "mini_histogram": check_is_NaN,
            "mode": False,
            "n_missing": 1,
            "p_missing": 0.11111111111111116,
            "p_unique": 2 / 8,
            "p_zeros": check_is_NaN,
            "range": check_is_NaN,
            "skewness": check_is_NaN,
            "std": check_is_NaN,
            "sum": check_is_NaN,
            "top": False,
            "type": Variable.TYPE_BOOL,
            "variance": check_is_NaN,
        },
        "bool_01": {
            "25%": check_is_NaN,
            "5%": check_is_NaN,
            "50%": check_is_NaN,
            "75%": check_is_NaN,
            "95%": check_is_NaN,
            "count": 9,
            "cv": check_is_NaN,
            "distinct_count": 2,
            "freq": 5,
            "histogram": check_is_NaN,
            "iqr": check_is_NaN,
            "is_unique": False,
            "kurtosis": check_is_NaN,
            "mad": check_is_NaN,
            "max": check_is_NaN,
            "min": check_is_NaN,
            "mini_histogram": check_is_NaN,
            "mode": True,
            "n_missing": 0,
            "p_missing": 0,
            "p_unique": 2 / 9,
            "p_zeros": check_is_NaN,
            "range": check_is_NaN,
            "skewness": check_is_NaN,
            "std": check_is_NaN,
            "sum": check_is_NaN,
            "top": 1,
            "type": Variable.TYPE_BOOL,
            "variance": check_is_NaN,
        },
        "bool_01_with_nan": {
            "25%": check_is_NaN,
            "5%": check_is_NaN,
            "50%": check_is_NaN,
            "75%": check_is_NaN,
            "95%": check_is_NaN,
            "count": 8,
            "cv": check_is_NaN,
            "distinct_count": 2,
            "freq": 4,
            "iqr": check_is_NaN,
            "is_unique": False,
            "kurtosis": check_is_NaN,
            "mad": check_is_NaN,
            "max": check_is_NaN,
            "min": check_is_NaN,
            "mode": False,
            "n_missing": 1,
            "p_missing": 0.11111111111111116,
            "p_unique": 2 / 8,
            "p_zeros": check_is_NaN,
            "range": check_is_NaN,
            "skewness": check_is_NaN,
            "std": check_is_NaN,
            "sum": check_is_NaN,
            "top": 0,
            "type": Variable.TYPE_BOOL,
            "variance": check_is_NaN,
        },
        "list": {
            "count": 9,
            "n_missing": 0,
            "p_missing": 0,
            "type": Variable.S_TYPE_UNSUPPORTED,
        },
        "mixed": {
            "count": 9,
            "n_missing": 0,
            "p_missing": 0,
            "type": Variable.S_TYPE_UNSUPPORTED,
        },
        "dict": {
            "count": 9,
            "n_missing": 0,
            "p_missing": 0,
            "type": Variable.S_TYPE_UNSUPPORTED,
        },
        "tuple": {
            "count": 9,
            "n_missing": 0,
            "p_missing": 0,
            "type": Variable.S_TYPE_UNSUPPORTED,
        },
    }


def test_describe_df(describe_data, expected_results):
    config["vars"]["num"]["low_categorical_threshold"].set(0)
    describe_data_frame = pd.DataFrame(describe_data)
    describe_data_frame["somedate"] = pd.to_datetime(describe_data_frame["somedate"])

    results = describe(describe_data_frame)

    assert {
        "table",
        "variables",
        "correlations",
        "missing",
        "messages",
        "scatter",
        "package",
    } == set(results.keys()), "Not in results"

    assert {"BOOL": 5, "CAT": 3, "UNSUPPORTED": 4, "NUM": 2, "DATE": 1} == results[
        "table"
    ]["types"], "Variable analysis failed"

    # Loop over variables
    for col in describe_data.keys():
        for k, v in expected_results[col].items():
            if v == check_is_NaN:
                assert (
                    k not in results["variables"][col]
                ) == True, "Value `{}` for key `{}` in column `{}` is not NaN".format(
                    results["variables"][col][k], k, col
                )
            elif isinstance(v, float):
                assert (
                    pytest.approx(v) == results["variables"][col][k]
                ), "Value `{}` for key `{}` in column `{}` is not NaN".format(
                    results["variables"][col][k], k, col
                )
            else:
                assert (
                    v == results["variables"][col][k]
                ), "Value `{}` for key `{}` in column `{}` is not NaN".format(
                    results["variables"][col][k], k, col
                )

        if results["variables"][col]["type"].value in ["NUM", "DATE"]:
            assert (
                "histogram_data" in results["variables"][col]
            ), "Mini-histogram missing for column {} ".format(col)


def test_describe_empty():
    empty_frame = pd.DataFrame()
    with pytest.raises(ValueError):
        describe(empty_frame)


def test_describe_list():
    with pytest.raises(AttributeError):
        with pytest.warns(UserWarning):
            describe([1, 2, 3])
