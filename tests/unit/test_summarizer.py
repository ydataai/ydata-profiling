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

    _ = format_summary(
        pps.summarize(pd.Series([1, 2, 3, 4, 5]), engine="pandas", dtype=Unsupported)
    )
    _ = format_summary(
        pps.summarize(pd.Series([1, 2, 3, 4, 5]), engine="pandas", dtype=Numeric)
    )
    _ = format_summary(
        pps.summarize(
            pd.Series(pd.date_range(start="1/1/2018", end="1/08/2018")),
            engine="pandas",
            dtype=DateTime,
        )
    )
    _ = format_summary(
        pps.summarize(
            pd.Series(["abc", "abc", "abba"]), engine="pandas", dtype=Categorical
        )
    )
    _ = format_summary(
        pps.summarize(
            pd.Series(["https://www.example.com"]), engine="pandas", dtype=URL
        )
    )
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
            engine="pandas",
            dtype=Path,
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
            engine="pandas",
            dtype=File,
        )
    )
    _ = format_summary(
        pps.summarize(
            pd.Series(
                [os.path.abspath(base_path + r"../../../docsrc/assets/lambda-labs.png")]
            ),
            engine="pandas",
            dtype=Image,
        )
    )
    _ = format_summary(
        pps.summarize(pd.Series([True, False, True, False, False]), "pandas", Boolean)
    )
