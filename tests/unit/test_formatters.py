import numpy as np
import pytest

from ydata_profiling.report.formatters import (
    fmt_array,
    fmt_bytesize,
    fmt_class,
    fmt_color,
    fmt_monotonic,
    fmt_numeric,
)


@pytest.mark.parametrize(
    "text, color, expected",
    [("This is a warning", "red", '<span style="color:red">This is a warning</span>')],
)
def test_fmt_color(text, color, expected):
    assert fmt_color(text, color) == expected


@pytest.mark.parametrize(
    "text, cls, expected",
    [
        (
            "This text is muted",
            "text-muted",
            '<span class="text-muted">This text is muted</span>',
        )
    ],
)
def test_fmt_class(text, cls, expected):
    assert fmt_class(text, cls) == expected


@pytest.mark.parametrize(
    "num, fmt, expected",
    [
        (0, None, "0.0 B"),
        (100, "Bytes", "100.0 Bytes"),
        (1024, None, "1.0 KiB"),
        (1024.0, None, "1.0 KiB"),
        (1024**4, "Bytes", "1.0 TiBytes"),
        (1024**3 * 7.5, None, "7.5 GiB"),
        (1024**8, None, "1.0 YiB"),
    ],
)
def test_fmt_bytesize(num, fmt, expected):
    if fmt is None:
        assert fmt_bytesize(num) == expected
    else:
        assert fmt_bytesize(num, fmt) == expected


@pytest.mark.parametrize(
    "array, threshold, expected",
    [
        (np.array([1, 2, 3], dtype=np.int16), 3, "[1 2 3]"),
        (
            np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], dtype=np.float32),
            1,
            "[ 1. ... 10.]",
        ),
        (
            np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], dtype=np.float32),
            3,
            "[ 1.  2.  3. ...  8.  9. 10.]",
        ),
    ],
)
def test_fmt_array(array, threshold, expected):
    assert fmt_array(array, threshold) == expected


@pytest.mark.parametrize(
    "value, precision, expected",
    [
        (79.999531, 3, "80"),
        (79.999531, 10, "79.999531"),
        (81.000000, 10, "81"),
        (81, 10, "81"),
        (81.999861123123123123, 10, "81.99986112"),
        (1e20, 10, "1 × 10<sup>20</sup>"),
        (1e-20, 10, "1 × 10<sup>-20</sup>"),
        (1e8, 3, "1 × 10<sup>8</sup>"),
    ],
)
def test_fmt_numeric(value, precision, expected):
    assert fmt_numeric(value, precision) == expected


@pytest.mark.parametrize(
    "value, expected",
    [
        (-2, "Strictly decreasing"),
        (-1, "Decreasing"),
        (0, "Not monotonic"),
        (1, "Increasing"),
        (2, "Strictly increasing"),
    ],
)
def test_fmt_monotonic(value, expected):
    assert fmt_monotonic(value) == expected


@pytest.mark.parametrize(
    "value",
    [
        -3,
        3,
    ],
)
def test_fmt_monotonic_err(value):
    with pytest.raises(ValueError):
        fmt_monotonic(value)
