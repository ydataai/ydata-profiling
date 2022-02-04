import pytest
import pandas as pd

from pandas_profiling.config import Settings
from pandas_profiling.model.summary_algorithms import histogram_spark_compute

@pytest.mark.sparktest
def test_histogram_spark_num(spark_session):
    cfg = Settings()
    df = pd.DataFrame({'x': [50, 50, -10, 0, 0, 5, 15, -3, None]})
    sdf = spark_session.createDataFrame(df)
    bin_data, bins = histogram_spark_compute(cfg, sdf, min(df.x), max(df.x), df.x.nunique())
    assert bin_data.to_dict() == {-10.: 2., 0.: 3., 10.: 1., 20.: 0., 30.: 0., 40.: 2.}
    assert bins == 6


@pytest.mark.sparktest
def test_histogram_spark_date(spark_session):
    cfg = Settings()
    from datetime import date, datetime
    df = pd.DataFrame({'somedate': [date(2011, 7, 4), datetime(2022, 1, 1, 13, 57),
                                    datetime(1990, 12, 9), None,
                                    datetime(1990, 12, 9), datetime(1950, 12, 9),
                                    datetime(1898, 1, 2), datetime(1950, 12, 9),
                                    datetime(1950, 12, 9)]})
    sdf = spark_session.createDataFrame(df)
    bin_data, bins = histogram_spark_compute(cfg,
                                             sdf,
                                             min(df.somedate),
                                             max(df.somedate),
                                             df.somedate.nunique())

    assert bin_data.to_dict() == {datetime(1898, 1, 2): 1,
                                  datetime(1922, 10, 21, 21, 59, 24): 0,
                                  datetime(1947, 8, 9, 19, 58, 48): 3,
                                  datetime(1972, 5, 27, 17, 58, 12): 2,
                                  datetime(1997, 3, 15, 15, 57, 36): 2}
    assert bins == 5