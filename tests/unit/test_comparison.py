import numpy as np
import pandas as pd
import pytest

from ydata_profiling import ProfileReport, compare
from ydata_profiling.compare_reports import _compare_title


@pytest.fixture()
def reports():
    df = pd.DataFrame(["a", "b", "c"])
    reports = [ProfileReport(df, title=f"report {idx}") for idx in range(5)]
    return reports


def test_compare_single(reports):
    with pytest.raises(ValueError) as e:
        args = reports[:1]
        assert len(args) == 1
        compare(args)
    assert e.value.args[0] == "At least two reports are required for this comparison"


def test_compare_two(reports):
    args = reports[:2]
    assert len(args) == 2
    result = compare(args)
    result_description = result.get_description()
    assert len(result_description["table"]["n"]) == 2


def test_compare_two_description(reports):
    args = [r.get_description() for r in reports[:2]]
    assert len(args) == 2
    result = compare(args)
    result_description = result.get_description()
    assert len(result_description["table"]["n"]) == 2


def test_compare_three(reports):
    args = reports[:3]
    assert len(args) == 3
    result = compare(args)
    result_description = result.get_description()
    assert len(result_description["table"]["n"]) == 3


def test_compare_three_description(reports):
    args = [r.get_description() for r in reports[:3]]
    assert len(args) == 3
    result = compare(args)
    result_description = result.get_description()
    assert len(result_description["table"]["n"]) == 3


def test_title():
    assert _compare_title(["a"]) == "a"
    assert _compare_title(["a", "b"]) == "<em>Comparing</em> a <em>and</em> b"
    assert _compare_title(["a", "b", "c"]) == "<em>Comparing</em> a, b <em>and</em> c"


def test_generate_comparison():
    size = 100
    df1 = pd.DataFrame({"a": np.arange(size)})
    df2 = pd.DataFrame({"a": np.arange(size)})

    p1 = ProfileReport(df1, title="p1")
    p2 = ProfileReport(df2, title="p1")
    html = p1.compare(p2).to_html()
    assert len(html) > 0
