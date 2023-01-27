import logging
import warnings
from datetime import date, datetime

import numpy as np
import pandas as pd
from matplotlib import MatplotlibDeprecationWarning
from pyspark.sql import SparkSession

from ydata_profiling import ProfileReport
from ydata_profiling.config import Settings

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    spark_session = (
        SparkSession.builder.appName("SparkProfiling").master("local[*]").getOrCreate()
    )

    print(spark_session.sparkContext.uiWebUrl)  # noqa: T201

    correlation_testdata = pd.DataFrame(
        {
            "test_num_1": [1, 2, 3, 5, 7, 8, 9, -100, -20, -np.inf, 3],
            "test_num_2": [11, 12, 13, 15, 17, 18, 4, 1, 4, 10, 20],
            "test_num_na1": [1, np.nan, 3, 5, 7, 8, np.nan, 1, np.nan, np.nan, np.nan],
            "test_num_na2": [11, np.nan, 13, 15, 17, 18, 4, 11, 1, 2, 3],
            "test_num_na3": [11, np.nan, 13, 15, 17, 18, 4, 11, np.nan, 4, 4],
            "test_cat_1": [
                "one",
                "one",
                "one",
                "two",
                "four",
                "four",
                "five",
                "seven",
                "seven",
                "seven",
                "one",
            ],
            "test_cat_2": [
                "one",
                "one",
                "two",
                "two",
                "three",
                "four",
                "four",
                "two",
                "seven",
                None,
                None,
            ],
            "test_cat_3": [
                "one",
                "one",
                "two",
                "two",
                "three",
                "four",
                "four",
                "two",
                "one",
                "one",
                "one",
            ],
            "test_bool": [
                True,
                False,
                True,
                False,
                True,
                False,
                True,
                False,
                True,
                False,
                True,
            ],
            "test_date": [
                date(2019, 5, 11),
                date(2019, 5, 12),
                date(2019, 5, 14),
                date(2019, 5, 14),
                date(2019, 5, 14),
                date(2019, 5, 11),
                date(2019, 5, 11),
                date(2019, 5, 12),
                date(2019, 5, 11),
                date(2019, 5, 11),
                date(2019, 5, 10),
            ],
            "test_datetime": [datetime(2019, 5, 11, 3, 3, 3)] * 11,
        }
    )
    upscale = 100
    if upscale > 1:
        correlation_testdata = pd.concat([correlation_testdata] * upscale)

    correlation_data_num = spark_session.createDataFrame(correlation_testdata)

    cfg = Settings()
    cfg.infer_dtypes = False
    cfg.correlations["auto"].calculate = False
    cfg.correlations["pearson"].calculate = True
    cfg.correlations["spearman"].calculate = True
    cfg.interactions.continuous = False
    cfg.missing_diagrams["bar"] = False
    cfg.missing_diagrams["heatmap"] = False
    cfg.missing_diagrams["matrix"] = False
    cfg.samples.tail = 0
    cfg.samples.random = 0

    # Create and start the monitoring process
    warnings.filterwarnings("ignore", category=MatplotlibDeprecationWarning)

    a = ProfileReport(
        correlation_data_num.toPandas(),
        correlations={
            "auto": {"calculate": True},
            "pearson": {"calculate": False},
            "spearman": {"calculate": False},
            "kendall": {"calculate": True},
            "phi_k": {"calculate": True},
            "cramers": {"calculate": False},
        },
    )

    a.to_file("test.html")
