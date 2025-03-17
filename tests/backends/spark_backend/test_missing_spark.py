from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from ydata_profiling.config import Settings
from ydata_profiling.model.spark.missing_spark import missing_bar


@pytest.fixture
def missing_data(spark_session):
    missing_testdata = pd.DataFrame(
        {
            "test_num_1": [1, np.nan, 3, 5, 7, 8, np.nan, 1],
            "test_num_2": [11, np.nan, 13, 15, 17, 18, 4, 11],
            "test_num_3": [11, np.nan, 13, 15, 17, 18, 4, 11],
        }
    )

    return spark_session.createDataFrame(missing_testdata)


def test_spark_missing_bar(missing_data):
    cfg = Settings()
    a = missing_bar(cfg, missing_data)

    Path("test.svg").write_text(a)
