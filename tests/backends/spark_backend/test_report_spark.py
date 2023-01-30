import pandas as pd
import pytest

from ydata_profiling import ProfileReport


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

    a = ProfileReport(correlation_data_num)

    a.to_file("test.html", silent=False)
