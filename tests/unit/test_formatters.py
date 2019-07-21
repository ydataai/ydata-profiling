import pytest
import numpy as np

from pandas_profiling.view.formatters import (
    fmt_color,
    fmt_class,
    fmt_bytesize,
    fmt_array,
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
        (1024 ** 4, "Bytes", "1.0 TiBytes"),
        (1024 ** 3 * 7.5, None, "7.5 GiB"),
        (1024 ** 8, None, "1.0 YiB"),
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
            "[ 1.  2.  3....  8.  9. 10.]",
        ),
    ],
)
def test_fmt_array(array, threshold, expected):
    assert fmt_array(array, threshold) == expected
