import json

import pandas as pd
import pytest

from pandas_profiling import ProfileReport


@pytest.fixture
def data():
    return pd.DataFrame(data={"col1": [1, 2], "col2": [3, 4]})


def test_json(data):
    report = ProfileReport(data)
    report_json = report.to_json()
    data = json.loads(report_json)
    assert set(data.keys()) == {
        "analysis",
        "correlations",
        "duplicates",
        "alerts",
        "missing",
        "package",
        "sample",
        "scatter",
        "table",
        "variables",
    }


def test_repr(data):
    report = ProfileReport(data)
    assert repr(report) == ""
