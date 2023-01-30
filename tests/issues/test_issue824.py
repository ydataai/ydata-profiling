"""
Test for issue 824:
https://github.com/ydataai/ydata-profiling/issues/824

High correlation warning printed multiple times

Problem :
The alert is probably generated for each active correlation calculation

Solution :
Field will be marked once is labelled as highly correlated for any calculation
"""
import pandas as pd
import pytest

from ydata_profiling import ProfileReport
from ydata_profiling.model.alerts import AlertType


@pytest.mark.skip()
def test_issue824():

    # Minimal reproducible code

    df = pd.DataFrame.from_dict(
        {
            "integer1": pd.Series([3, 4, 5, 6], dtype="int"),
            "integer2": pd.Series([3, 4, 5, 6], dtype="int"),
            "integer3": pd.Series([3, 4, 5, 6], dtype="int"),
            "integer4": pd.Series([3, 4, 5, 6], dtype="int"),
            "integer5": pd.Series([3, 4, 5, 6], dtype="int"),
        }
    )

    report = ProfileReport(df)
    _ = report.description_set

    assert (
        len(
            [
                a
                for a in report.description_set["alerts"]
                if a.alert_type == AlertType.HIGH_CORRELATION
            ]
        )
        == 5
    )
