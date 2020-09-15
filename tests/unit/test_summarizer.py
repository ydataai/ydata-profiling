import os

import pandas as pd

from pandas_profiling.model.summarizer import PandasProfilingSummarizer, format_summary
from pandas_profiling.model.typeset import (
    URL,
    Boolean,
    Categorical,
    DateTime,
    File,
    Image,
    Numeric,
    Path,
    ProfilingTypeSet,
    Unsupported,
)

base_path = os.path.abspath(os.path.dirname(__file__))


def test_summarizer():
    pps = PandasProfilingSummarizer(typeset=ProfilingTypeSet())

    _ = format_summary(pps.summarize(pd.Series([1, 2, 3, 4, 5]), Unsupported))
    _ = format_summary(pps.summarize(pd.Series([1, 2, 3, 4, 5]), Numeric))
    _ = format_summary(
        pps.summarize(
            pd.Series(pd.date_range(start="1/1/2018", end="1/08/2018")), DateTime
        )
    )
    _ = format_summary(pps.summarize(pd.Series(["abc", "abc", "abba"]), Categorical))
    _ = format_summary(pps.summarize(pd.Series(["https://www.example.com"]), URL))
    _ = format_summary(
        pps.summarize(
            pd.Series(
                [
                    os.path.abspath(
                        base_path
                        + r"../../../src/pandas_profiling/model/typeset_does_not_exist.py"
                    )
                ]
            ),
            Path,
        )
    )
    _ = format_summary(
        pps.summarize(
            pd.Series(
                [
                    os.path.abspath(
                        base_path + r"../../../src/pandas_profiling/model/typeset.py"
                    )
                ]
            ),
            File,
        )
    )
    _ = format_summary(
        pps.summarize(
            pd.Series(
                [os.path.abspath(base_path + r"../../../docsrc/assets/lambda-labs.png")]
            ),
            Image,
        )
    )
    _ = format_summary(
        pps.summarize(pd.Series([True, False, True, False, False]), Boolean)
    )
