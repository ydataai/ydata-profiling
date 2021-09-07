import pandas as pd
import pytest

from pandas_profiling import ProfileReport
from pandas_profiling.config import Settings


@pytest.fixture
def correlation_data_num(spark_session):
    correlation_testdata = pd.DataFrame(
        {
            "test_num_1": [1, 2, 3, 5, 7, 8, 9],
            "test_num_2": [11, 12, 13, 15, 17, 18, 4],
        }
    )

    return spark_session.createDataFrame(correlation_testdata)


def test_report_spark(correlation_data_num):
    cfg = Settings()
    cfg.infer_dtypes = False
    cfg.correlations["kendall"].calculate = False
    cfg.correlations["cramers"].calculate = False
    cfg.correlations["phi_k"].calculate = False

    a = ProfileReport(correlation_data_num, config=cfg)
    a.to_file("test.html", silent=False)
