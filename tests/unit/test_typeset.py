import datetime
import os

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
    get_series,
    infers,
)

base_path = os.path.abspath(os.path.dirname(__file__))


def get_profiling_series():
    data = {
        # Boolean
        "booleans_type": [False, True, True],
        "booleans_type_nan": [False, True, np.nan],
        "str_yes_no": ["Y", "N", "Y"],
        "str_yes_no_mixed": ["Y", "n", "y"],
        "str_yes_no_nan": ["Y", "N", np.nan],
        "str_true_false": ["True", "False", "False"],
        "str_true_false_nan": ["True", "False", np.nan],
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
    }

    series = pd.DataFrame(data)
    return series


# return {
#     "id": Categorical,
#     "x": Numeric,
#     "y": Numeric,
#     "cat": Categorical,
#     "s1": Boolean,
#     "s2": Categorical,
#     "somedate": DateTime,
#     "bool_tf": Boolean,
#     "bool_tf_with_nan": Boolean,
#     "bool_01": Categorical,
#     "bool_01_with_nan": Categorical,
#     "list": Unsupported,
#     "mixed": Unsupported,
#     "dict": Unsupported,
#     "tuple": Unsupported,
# }

series = get_series()

typeset = ProfilingTypeSet()

contains_map = {
    Numeric: {
        "int_series",
        "Int64_int_series",
        "int_range",
        "Int64_int_nan_series",
        "int_series_boolean",
        "np_uint32",
        "pd_uint32",
        "float_series",
        "float_series2",
        "float_series3",
        "float_series4",
        "inf_series",
        "float_nan_series",
        "float_series5",
        "int_nan_series",
        "float_with_inf",
        "float_series6",
        "complex_series",
        "complex_series_py",
        "complex_series_nan",
        "complex_series_py_nan",
        "complex_series_nan_2",
        "complex_series_float",
    },
    Categorical: {
        "categorical_int_series",
        "categorical_float_series",
        "categorical_string_series",
        "categorical_complex_series",
        "categorical_char",
        "ordinal",
        "timestamp_string_series",
        "string_with_sep_num_nan",
        "string_series",
        "geometry_string_series",
        "string_unicode_series",
        "string_np_unicode_series",
        "path_series_linux_str",
        "path_series_windows_str",
        "int_str_range",
        "string_date",
        "textual_float",
        "textual_float_nan",
        "ip_str",
        "string_flt",
        "string_num",
        "str_url",
        "string_str_nan",
        "string_num_nan",
        "string_bool_nan",
        "string_flt_nan",
        "str_complex",
        "uuid_series_str",
        "str_int_leading_zeros",
        "email_address_str",
        "str_float_non_leading_zeros",
        "str_int_zeros",
        "mixed",
        "bool_nan_series",
    },
    Boolean: {
        "bool_series",
        "bool_series2",
        "bool_series3",
        "nullable_bool_series",
    },
    DateTime: {
        "timestamp_series",
        "timestamp_aware_series",
        "datetime",
        "timestamp_series_nat",
        "date_series_nat",
    },
}

if int(pd.__version__[0]) >= 1:
    contains_map[Categorical].add("string_dtype_series")

contains_map[Categorical] = contains_map[Categorical].union(contains_map[Boolean])
contains_map[Unsupported] = {
    "nan_series",
    "nan_series_2",
    "timedelta_series",
    "timedelta_series_nat",
    "timedelta_negative",
    "path_series_linux",
    "path_series_linux_missing",
    "path_series_windows",
    "url_series",
    "url_nan_series",
    "url_none_series",
    "file_test_py",
    "file_mixed_ext",
    "file_test_py_missing",
    "image_png",
    "image_png_missing",
    "image_png",
    "image_png_missing",
    "uuid_series",
    "uuid_series_missing",
    "mixed_list[str,int]",
    "mixed_dict",
    "callable",
    "mixed_integer",
    "mixed_list",
    "date",
    "time",
    "empty",
    "empty_bool",
    "empty_float",
    "empty_int64",
    "empty_object",
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
    "int_series": Numeric,
    "categorical_int_series": Numeric,
    "int_nan_series": Numeric,
    "Int64_int_series": Numeric,
    "Int64_int_nan_series": Numeric,
    "np_uint32": Numeric,
    "pd_uint32": Numeric,
    "int_range": Numeric,
    "float_series": Numeric,
    "float_nan_series": Numeric,
    "int_series_boolean": Numeric,
    "float_series2": Numeric,
    "float_series3": Numeric,
    "float_series4": Numeric,
    "float_series5": Numeric,
    "float_series6": Numeric,
    "complex_series_float": Numeric,
    "categorical_float_series": Categorical,
    "float_with_inf": Numeric,
    "inf_series": Numeric,
    "nan_series": Unsupported,
    "nan_series_2": Unsupported,
    "string_series": Categorical,
    "categorical_string_series": Categorical,
    "timestamp_string_series": Categorical,
    "string_with_sep_num_nan": Categorical,  # TODO: Introduce thousands separator
    "string_unicode_series": Categorical,
    "string_np_unicode_series": Categorical,
    "string_num_nan": Numeric,
    "string_num": Numeric,
    "string_flt_nan": Numeric,
    "string_flt": Numeric,
    "string_str_nan": Categorical,
    "string_bool_nan": Boolean,
    "int_str_range": Numeric,
    "string_date": Categorical,
    "str_url": Categorical,
    "bool_series": Boolean,
    "bool_nan_series": Boolean,
    "nullable_bool_series": Boolean,
    "bool_series2": Boolean,
    "bool_series3": Boolean,
    "complex_series": Numeric,
    "complex_series_nan": Numeric,
    "complex_series_nan_2": Numeric,
    "complex_series_py_nan": Numeric,
    "complex_series_py": Numeric,
    "categorical_complex_series": Numeric,
    "timestamp_series": DateTime,
    "timestamp_series_nat": DateTime,
    "timestamp_aware_series": DateTime,
    "datetime": DateTime,
    "timedelta_series": Unsupported,
    "timedelta_series_nat": Unsupported,
    "timedelta_negative": Unsupported,
    "geometry_string_series": Categorical,
    "geometry_series_missing": Unsupported,
    "geometry_series": Unsupported,
    "path_series_linux": Unsupported,
    "path_series_linux_missing": Unsupported,
    "path_series_linux_str": Categorical,
    "path_series_windows": Unsupported,
    "path_series_windows_str": Categorical,
    "url_series": Unsupported,
    "url_nan_series": Unsupported,
    "url_none_series": Unsupported,
    "mixed_list[str,int]": Unsupported,
    "mixed_dict": Unsupported,
    "mixed_integer": Unsupported,
    "mixed_list": Unsupported,
    "mixed": Boolean,
    "callable": Unsupported,
    "module": Unsupported,
    "textual_float": Numeric,
    "textual_float_nan": Numeric,
    "empty": Unsupported,
    "empty_object": Unsupported,
    "empty_float": Unsupported,
    "empty_bool": Unsupported,
    "empty_int64": Unsupported,
    "ip": Unsupported,
    "ip_str": Categorical,
    "ip_missing": Unsupported,
    "date_series_nat": DateTime,
    "date": Unsupported,
    "time": Unsupported,
    "categorical_char": Categorical,
    "ordinal": Categorical,
    "str_complex": Categorical,
    "uuid_series": Unsupported,
    "uuid_series_str": Categorical,
    "uuid_series_missing": Unsupported,
    "ip_mixed_v4andv6": Unsupported,
    "file_test_py": Unsupported,
    "file_test_py_missing": Unsupported,
    "file_mixed_ext": Unsupported,
    "image_png": Unsupported,
    "image_png_missing": Unsupported,
    "str_int_leading_zeros": Numeric,
    "str_float_non_leading_zeros": Numeric,
    "str_int_zeros": Numeric,
    "email_address_str": Categorical,
}
if int(pd.__version__[0]) >= 1:
    inference_map["string_dtype_series"] = Categorical


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
    (Categorical, Numeric, {"int_series", "mixed"}),
    (
        Numeric,
        Categorical,
        {
            "string_flt",
            "string_num_nan",
            "string_num",
            "string_flt_nan",
            "textual_float",
            "textual_float_nan",
            "int_str_range",
            "str_float_non_leading_zeros",
            "str_int_zeros",
            "mixed",
        },
    ),
    (
        Boolean,
        Categorical,
        {
            "string_bool_nan",
            "bool_series",
            "bool_series2",
            "bool_series3",
            "nullable_bool_series",
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
