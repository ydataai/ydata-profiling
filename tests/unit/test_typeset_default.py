import datetime
import os
import pathlib
import uuid
from ipaddress import IPv4Address, IPv6Address
from pathlib import PurePosixPath, PureWindowsPath
from urllib.parse import urlparse

import numpy as np
import pandas as pd
import pytest

# from visions.test.series import get_series
from visions.test.utils import (
    contains,
    convert,
    get_contains_cases,
    get_convert_cases,
    get_inference_cases,
    infers,
)
from visions.types.email_address import FQDA

from pandas_profiling.config import config
from pandas_profiling.model.typeset import (
    Boolean,
    Categorical,
    DateTime,
    Numeric,
    ProfilingTypeSet,
    Unsupported,
)

if int(pd.__version__.split(".")[0]) < 1:
    from visions.dtypes.boolean import BoolDtype

    btype = "Bool"
else:
    btype = "boolean"

base_path = os.path.abspath(os.path.dirname(__file__))


# Workaround pending release https://github.com/dylan-profiler/visions/issues/162
def get_series():
    test_series = [
        # Int Series
        pd.Series([1, 2, 3], name="int_series"),
        pd.Series(range(10), name="int_range"),
        pd.Series([1, 2, 3], name="Int64_int_series", dtype="Int64"),
        pd.Series([1, 2, 3, np.nan], name="Int64_int_nan_series", dtype="Int64"),
        pd.Series([1, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0], name="int_series_boolean"),
        # Count
        pd.Series(np.array([1, 2, 3, 4], dtype=np.uint32), name="np_uint32"),
        pd.Series([1, 2, 3, 4], dtype="UInt32", name="pd_uint32"),
        # Categorical
        pd.Series([1, 2, 3], name="categorical_int_series", dtype="category"),
        pd.Series(
            pd.Categorical(
                ["A", "B", "C", "C", "B", "A"],
                categories=["A", "B", "C"],
                ordered=False,
            ),
            name="categorical_char",
        ),
        pd.Series([1.0, 2.0, 3.1], dtype="category", name="categorical_float_series"),
        pd.Series(
            ["Georgia", "Sam"], dtype="category", name="categorical_string_series"
        ),
        pd.Series(
            [complex(0, 0), complex(1, 2), complex(3, -1)],
            name="categorical_complex_series",
            dtype="category",
        ),
        # Ordinal
        pd.Series(
            pd.Categorical(
                ["A", "B", "C", "C", "B", "A"], categories=["A", "B", "C"], ordered=True
            ),
            name="ordinal",
        ),
        # Float Series
        pd.Series([1.0, 2.1, 3.0], name="float_series"),
        pd.Series([1.0, 2.5, np.nan], name="float_nan_series"),
        pd.Series([1.0, 2.0, 3.0, 4.0], name="float_series2"),
        pd.Series(np.array([1.2, 2, 3, 4], dtype=np.float64), name="float_series3"),
        pd.Series([1, 2, 3.05, 4], dtype=np.float64, name="float_series4"),
        pd.Series([np.nan, 1.2], name="float_series5"),
        pd.Series([np.nan, 1.1], dtype=np.single, name="float_series6"),
        pd.Series([np.inf, np.NINF, np.PINF, 1000000.0, 5.5], name="float_with_inf"),
        pd.Series([np.inf, np.NINF, np.Infinity, np.PINF], name="inf_series"),
        pd.Series([1, 2, np.nan], name="int_nan_series"),
        # Nan Series
        pd.Series([np.nan], name="nan_series"),
        pd.Series([np.nan, np.nan, np.nan, np.nan], name="nan_series_2"),
        # String Series
        pd.Series(["Patty", "Valentine"], name="string_series"),
        pd.Series(["mack", "the", "finger"], name="string_unicode_series"),
        pd.Series(
            np.array(["upper", "hall"], dtype=np.unicode_),
            name="string_np_unicode_series",
        ),
        pd.Series(["1.0", "2.0", np.nan], name="string_num_nan"),
        pd.Series(["1,000.0", "2.1", np.nan], name="string_with_sep_num_nan"),
        pd.Series(["1.0", "2.0", "3.0"], name="string_num"),
        pd.Series(["1.0", "45.67", np.nan], name="string_flt_nan"),
        pd.Series(["1.0", "45.67", "3.5"], name="string_flt"),
        pd.Series(
            [
                "I was only robbing the register,",
                "I hope you understand",
                "One of us had better call up the cops",
                "In the hot New Jersey night",
                np.nan,
            ],
            name="string_str_nan",
        ),
        pd.Series(["True", "False", None], name="string_bool_nan"),
        pd.Series(range(20), name="int_str_range").astype("str"),
        pd.Series(
            [
                "http://www.cwi.nl:80/%7Eguido/Python.html",
                "https://github.com/dylan-profiling/hurricane",
            ],
            name="str_url",
        ),
        pd.Series(
            [r"C:\\home\\user\\file.txt", r"C:\\home\\user\\test2.txt"],
            name="path_series_windows_str",
        ),
        pd.Series(
            [r"/home/user/file.txt", r"/home/user/test2.txt"],
            name="path_series_linux_str",
        ),
        pd.Series(["0011", "12"], name="str_int_leading_zeros"),
        pd.Series(["0.0", "0.04", "0"], name="str_float_non_leading_zeros"),
        pd.Series(["0.0", "0.000", "0", "2"], name="str_int_zeros"),
        # Bool Series
        pd.Series([True, False], name="bool_series"),
        pd.Series([True, False, None], name="bool_nan_series"),
        pd.Series([True, False, None], name="nullable_bool_series", dtype=btype),
        pd.Series([True, False, False, True], name="bool_series2", dtype=bool),
        pd.Series([True, False, False, True], name="bool_series2", dtype=bool),
        pd.Series(np.array([1, 0, 0, 1], dtype=bool), name="bool_series3"),
        # Complex Series
        pd.Series(
            [complex(0, 0), complex(1, 2), complex(3, -1)],
            name="complex_series",
        ),
        pd.Series(
            [
                complex(0, 0),
                complex(1, 2),
                complex(3, -1),
                complex(np.nan, np.nan),
            ],
            name="complex_series_nan",
        ),
        pd.Series(["(1+1j)", "(2+2j)", "(10+100j)"], name="str_complex"),
        pd.Series(["(1+1j)", "(2+2j)", "(10+100j)", "NaN"], name="str_complex_nan"),
        pd.Series(
            [complex(0, 0), complex(1, 2), complex(3, -1), np.nan],
            name="complex_series_nan_2",
        ),
        pd.Series(
            [complex(0, 0), complex(1, 2), complex(3, -1), np.nan],
            name="complex_series_py_nan",
        ),
        pd.Series(
            [complex(0, 0), complex(1, 2), complex(3, -1)], name="complex_series_py"
        ),
        pd.Series(
            [
                complex(0, 0),
                complex(1, 0),
                complex(3, 0),
                complex(-1, 0),
            ],
            name="complex_series_float",
        ),
        # Datetime Series
        pd.Series(["1937-05-06", "20/4/2014"], name="string_date"),
        pd.Series(["1941-05-24", "13/10/2016"], name="timestamp_string_series"),
        pd.to_datetime(
            pd.Series(
                [datetime.datetime(2017, 3, 5, 12, 2), datetime.datetime(2019, 12, 4)],
                name="timestamp_series",
            )
        ),
        pd.to_datetime(
            pd.Series(
                [
                    datetime.datetime(2017, 3, 5),
                    datetime.datetime(2019, 12, 4, 3, 2, 0),
                    pd.NaT,
                ],
                name="timestamp_series_nat",
            )
        ),
        pd.to_datetime(
            pd.Series(
                [datetime.datetime(2017, 3, 5), datetime.datetime(2019, 12, 4), pd.NaT],
                name="date_series_nat",
            )
        ),
        pd.Series(
            pd.date_range(
                start="2013-05-18 12:00:01",
                periods=2,
                freq="H",
                tz="Europe/Brussels",
                name="timestamp_aware_series",
            )
        ),
        pd.to_datetime(
            pd.Series(
                [
                    datetime.date(2011, 1, 1),
                    datetime.date(2012, 1, 2),
                    datetime.date(2013, 1, 1),
                ],
                name="datetime",
            )
        ),
        # Date series
        pd.Series(
            [
                datetime.date(2011, 1, 1),
                datetime.date(2012, 1, 2),
                datetime.date(2013, 1, 1),
            ],
            name="date",
        ),
        # Time series
        pd.Series(
            [
                datetime.time(8, 43, 12),
                datetime.time(9, 43, 12),
                datetime.time(10, 43, 12),
            ],
            name="time",
        ),
        # http://pandas-docs.github.io/pandas-docs-travis/user_guide/timeseries.html#timestamp-limitations
        # pd.to_datetime(
        #     pd.Series(
        #         [
        #             datetime.datetime(year=1, month=1, day=1, hour=8, minute=43, second=12),
        #             datetime.datetime(year=1, month=1, day=1, hour=9, minute=43, second=12),
        #             datetime.datetime(
        #                 year=1, month=1, day=1, hour=10, minute=43, second=12
        #             ),
        #         ],
        #         name="datetime_to_time",
        #     )
        # ),
        # Timedelta Series
        pd.Series([pd.Timedelta(days=i) for i in range(3)], name="timedelta_series"),
        pd.Series(
            [pd.Timedelta(days=i) for i in range(3)] + [pd.NaT],
            name="timedelta_series_nat",
        ),
        pd.Series(
            [
                pd.Timedelta("1 days 00:03:43"),
                pd.Timedelta("5 days 12:33:57"),
                pd.Timedelta("0 days 01:25:07"),
                pd.Timedelta("-2 days 13:46:56"),
                pd.Timedelta("1 days 23:49:25"),
            ],
            name="timedelta_negative",
        ),
        # Path Series
        pd.Series(
            [
                PurePosixPath("/home/user/file.txt"),
                PurePosixPath("/home/user/test2.txt"),
            ],
            name="path_series_linux",
        ),
        pd.Series(
            [
                PurePosixPath("/home/user/file.txt"),
                PurePosixPath("/home/user/test2.txt"),
                None,
            ],
            name="path_series_linux_missing",
        ),
        pd.Series(
            [
                PureWindowsPath("C:\\home\\user\\file.txt"),
                PureWindowsPath("C:\\home\\user\\test2.txt"),
            ],
            name="path_series_windows",
        ),
        # Url Series
        pd.Series(
            [
                urlparse("http://www.cwi.nl:80/%7Eguido/Python.html"),
                urlparse("https://github.com/dylan-profiling/hurricane"),
            ],
            name="url_series",
        ),
        pd.Series(
            [
                urlparse("http://www.cwi.nl:80/%7Eguido/Python.html"),
                urlparse("https://github.com/dylan-profiling/hurricane"),
                np.nan,
            ],
            name="url_nan_series",
        ),
        pd.Series(
            [
                urlparse("http://www.cwi.nl:80/%7Eguido/Python.html"),
                urlparse("https://github.com/dylan-profiling/hurricane"),
                None,
            ],
            name="url_none_series",
        ),
        # UUID Series
        pd.Series(
            [
                uuid.UUID("0b8a22ca-80ad-4df5-85ac-fa49c44b7ede"),
                uuid.UUID("aaa381d6-8442-4f63-88c8-7c900e9a23c6"),
                uuid.UUID("00000000-0000-0000-0000-000000000000"),
            ],
            name="uuid_series",
        ),
        pd.Series(
            [
                uuid.UUID("0b8a22ca-80ad-4df5-85ac-fa49c44b7ede"),
                uuid.UUID("aaa381d6-8442-4f63-88c8-7c900e9a23c6"),
                uuid.UUID("00000000-0000-0000-0000-000000000000"),
                None,
            ],
            name="uuid_series_missing",
        ),
        pd.Series(
            [
                "0b8a22ca-80ad-4df5-85ac-fa49c44b7ede",
                "aaa381d6-8442-4f63-88c8-7c900e9a23c6",
                "00000000-0000-0000-0000-000000000000",
            ],
            name="uuid_series_str",
        ),
        # Object Series
        pd.Series([[1, ""], [2, "Rubin"], [3, "Carter"]], name="mixed_list[str,int]"),
        pd.Series(
            [{"why": "did you"}, {"bring him": "in for he"}, {"aint": "the guy"}],
            name="mixed_dict",
        ),
        pd.Series(
            [pd.to_datetime, pd.to_timedelta, pd.read_json, pd.to_pickle],
            name="callable",
        ),
        pd.Series([pd, np], name="module"),
        pd.Series(["1.1", "2"], name="textual_float"),
        pd.Series(["1.1", "2", "NAN"], name="textual_float_nan"),
        # Object (Mixed, https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.api.types.infer_dtype.html)
        pd.Series(["a", 1], name="mixed_integer"),
        pd.Series([True, False, np.nan], name="mixed"),
        pd.Series([[True], [False], [False]], name="mixed_list"),
        pd.Series([[1, ""], [2, "Rubin"], [3, "Carter"]], name="mixed_list[str,int]"),
        pd.Series(
            [{"why": "did you"}, {"bring him": "in for he"}, {"aint": "the guy"}],
            name="mixed_dict",
        ),
        # IP
        pd.Series([IPv4Address("127.0.0.1"), IPv4Address("127.0.0.1")], name="ip"),
        pd.Series(["127.0.0.1", "127.0.0.1"], name="ip_str"),
        # Empty
        pd.Series([], name="empty", dtype=np.float64),
        pd.Series([], name="empty_float", dtype=float),
        pd.Series([], name="empty_int64", dtype="Int64"),
        pd.Series([], name="empty_object", dtype="object"),
        pd.Series([], name="empty_bool", dtype=bool),
        # IP
        pd.Series([IPv4Address("127.0.0.1"), IPv4Address("127.0.0.1")], name="ip"),
        pd.Series(
            [IPv4Address("127.0.0.1"), None, IPv4Address("127.0.0.1")],
            name="ip_missing",
        ),
        pd.Series(
            [IPv6Address("0:0:0:0:0:0:0:1"), IPv4Address("127.0.0.1")],
            name="ip_mixed_v4andv6",
        ),
        pd.Series(["127.0.0.1", "127.0.0.1"], name="ip_str"),
        # File
        pd.Series(
            [
                pathlib.Path(os.path.join(base_path, "series.py")).absolute(),
                pathlib.Path(os.path.join(base_path, "__init__.py")).absolute(),
                pathlib.Path(os.path.join(base_path, "utils.py")).absolute(),
            ],
            name="file_test_py",
        ),
        pd.Series(
            [
                pathlib.Path(os.path.join(base_path, "..", "py.typed")).absolute(),
                pathlib.Path(
                    os.path.join(
                        base_path, "..", "visualisation", "circular_packing.html"
                    )
                ).absolute(),
                pathlib.Path(os.path.join(base_path, "series.py")).absolute(),
            ],
            name="file_mixed_ext",
        ),
        pd.Series(
            [
                pathlib.Path(os.path.join(base_path, "series.py")).absolute(),
                None,
                pathlib.Path(os.path.join(base_path, "__init__.py")).absolute(),
                None,
                pathlib.Path(os.path.join(base_path, "utils.py")).absolute(),
            ],
            name="file_test_py_missing",
        ),
        # Image
        pd.Series(
            [
                pathlib.Path(
                    os.path.join(
                        base_path,
                        "../visualisation/typesets/typeset_complete.png",
                    )
                ).absolute(),
                pathlib.Path(
                    os.path.join(
                        base_path,
                        r"../visualisation/typesets/typeset_standard.png",
                    )
                ).absolute(),
                pathlib.Path(
                    os.path.join(
                        base_path,
                        r"../visualisation/typesets/typeset_geometry.png",
                    )
                ).absolute(),
            ],
            name="image_png",
        ),
        pd.Series(
            [
                pathlib.Path(
                    os.path.join(
                        base_path,
                        r"../visualisation/typesets/typeset_complete.png",
                    )
                ).absolute(),
                pathlib.Path(
                    os.path.join(
                        base_path,
                        r"../visualisation/typesets/typeset_standard.png",
                    )
                ).absolute(),
                None,
                pathlib.Path(
                    os.path.join(
                        base_path,
                        r"../visualisation/typesets/typeset_geometry.png",
                    )
                ).absolute(),
                None,
            ],
            name="image_png_missing",
        ),
        # Email
        pd.Series(
            [FQDA("test", "example.com"), FQDA("info", "example.eu")],
            name="email_address",
        ),
        pd.Series(
            [FQDA("test", "example.com"), FQDA("info", "example.eu"), None],
            name="email_address_missing",
        ),
        pd.Series(["test@example.com", "info@example.eu"], name="email_address_str"),
    ]

    if int(pd.__version__.split(".")[0]) >= 1:
        pandas_1_series = [
            pd.Series(
                ["Patty", "Valentine"], dtype="string", name="string_dtype_series"
            )
        ]
        test_series.extend(pandas_1_series)

    return test_series


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
        "str_complex_nan",
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
    "module",
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
    "empty_object",
    "empty_int64",
    "ip",
    "ip_missing",
    "ip_mixed_v4andv6",
    "email_address_missing",
    "email_address",
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
    "empty_object": Unsupported,
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
    "str_complex_nan": Categorical,
    "email_address": Unsupported,
    "email_address_missing": Unsupported,
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
