"""
Test for issue 215:
https://github.com/ydataai/ydata-profiling/issues/215
"""
import pytest

from ydata_profiling.report.formatters import fmt_percent


@pytest.mark.parametrize(
    "ratio, expected_formatting",
    [
        (0.01, "1.0%"),
        (0.001, "0.1%"),
        (0.0001, "< 0.1%"),
        (1.0, "100.0%"),
        (0.99999, "> 99.9%"),
    ],
)
def test_issue215(ratio, expected_formatting):
    assert fmt_percent(ratio) == expected_formatting
