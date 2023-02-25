import json

import pandas as pd
import pytest
from pandas_profiling import ProfileReport


@pytest.fixture
def data():
    return pd.DataFrame(data={"col1": [1, 2], "col2": [3, 4]})


def test_json(data: pd.DataFrame):
    report = ProfileReport(data)
    report_json = report.to_json()
    data = json.loads(report_json)
    assert set(data.keys()) == {
        "analysis",
        "target",
        "variables",
        "correlations",
        "duplicates",
        "alerts",
        "missing",
        "package",
        "sample",
        "scatter",
        "table",
    }


def test_repr(data):
    report = ProfileReport(data)
    assert repr(report) == ""
