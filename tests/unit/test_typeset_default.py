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
        "categorical_float_series",
        "categorical_int_series",
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
    },
    Boolean: {
        "bool_series",
        "bool_series2",
        "bool_series3",
        "nullable_bool_series",
        "mixed",
        "bool_nan_series",
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
    "categorical_float_series": Numeric,
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
    (Categorical, Numeric, {"mixed"}),
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
            "str_int_leading_zeros",
            "mixed",
            "categorical_complex_series",
            "int_series",
            "categorical_int_series",
            "categorical_float_series",
        },
    ),
    (
        Boolean,
        Categorical,
        {
            "string_bool_nan",
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
    config["vars"]["num"]["low_categorical_threshold"].set(0)
    result, message = convert(source_type, relation_type, series, member)
    assert result, message
