import datetime

import numpy as np
import pandas as pd
import pytest

from pandas_profiling.config import config
from pandas_profiling.model.typeset import (
    Boolean,
    Categorical,
    DateTime,
    Numeric,
    ProfilingTypeSet,
    Unsupported,
)
from tests.unit.utils import (
    contains,
    convert,
    get_contains_cases,
    get_convert_cases,
    get_inference_cases,
    infers,
)


def get_profiling_series():
    data = {
        "empty": [],
        # Boolean
        "booleans_type": [False, True, True],
        "booleans_type_nan": [False, True, np.nan],
        "str_yes_no": ["Y", "N", "Y"],
        "str_yes_no_mixed": ["Y", "n", "y"],
        "str_yes_no_nan": ["Y", "N", np.nan],
        "str_true_false": ["True", "False", "False"],
        "str_true_false_nan": ["True", "False", np.nan],
        "str_true_false_none": ["True", "False", None],
        # Numeric
        "num_with_inf": [1, 2, 3, 6, np.inf],
        "integers": [1, 0, 0],
        "integers_nan": [1, 0, np.nan],
        # test Describe
        "id": [chr(97 + c) for c in range(1, 9)] + ["d"],
        "x": [50, 50, -10, 0, 0, 5, 15, -3, np.nan],
        "y": [
            0.000001,
            654.152,
            np.nan,
            15.984512,
            3122,
            -3.1415926535,
            111,
            15.9,
            13.5,
        ],
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
        "date_str": ["2018-01-01", "2017-02-01", "2018-04-07"],
    }

    return [pd.Series(values, name=key) for key, values in data.items()]


# return {
#     "date_str": Categorical                   DateTime
# }

series = get_profiling_series()

typeset = ProfilingTypeSet()

contains_map = {
    Numeric: {
        "x",
        "y",
        "s1",
        "num_with_inf",
        "integers",
        "integers_nan",
        "bool_01",
        "bool_01_with_nan",
    },
    Categorical: {
        "id",
        "cat",
        "s2",
        "date_str",
    },
    Boolean: {
        "bool_tf",
        "bool_tf_with_nan",
        "booleans_type",
        "booleans_type_nan",
        "str_yes_no",
        "str_yes_no_mixed",
        "str_yes_no_nan",
        "str_true_false",
        "str_true_false_none",
        "str_true_false_nan",
    },
    DateTime: {
        "somedate",
    },
}

# if int(pd.__version__[0]) >= 1:
#     contains_map[Categorical].add("string_dtype_series")

# contains_map[Categorical] = contains_map[Categorical].union(contains_map[Boolean])
contains_map[Unsupported] = {
    "empty",
    "list",
    "mixed",
    "dict",
    "tuple"
}


@pytest.mark.parametrize(**get_contains_cases(series, contains_map, typeset))
def test_contains(series, type, member):
    """Test the generated combinations for "series in type"

    Args:
        series: the series to test
        type: the type to test against
        member: the result
    """
    config["vars"]["num"]["low_categorical_threshold"].set(0)
    result, message = contains(series, type, member)
    assert result, message


inference_map = {
    # "int_series": Numeric,
}


@pytest.mark.parametrize(**get_inference_cases(series, inference_map, typeset))
def test_inference(series, type, typeset, difference):
    """Test the generated combinations for "inference(series) == type"

    Args:
        series: the series to test
        type: the type to test against
    """
    config["vars"]["num"]["low_categorical_threshold"].set(0)
    result, message = infers(series, type, typeset, difference)
    assert result, message


# Conversions in one single step
convert_map = [
    # Model type, Relation type
    (Categorical, Numeric, {}),
    (
        Numeric,
        Categorical,
        {
        },
    ),
    (
        Boolean,
        Categorical,
        {
        },
    ),
]


@pytest.mark.parametrize(**get_convert_cases(series, convert_map, typeset))
def test_conversion(source_type, relation_type, series, member):
    """Test the generated combinations for "convert(series) == type" and "infer(series) = source_type"

    Args:
        series: the series to test
        type: the type to test against
    """
    result, message = convert(source_type, relation_type, series, member)
    assert result, message
