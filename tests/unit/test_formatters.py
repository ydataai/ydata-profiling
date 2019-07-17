import pytest

from pandas_profiling.view.formatters import fmt_color, fmt_class, fmt_bytesize


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
