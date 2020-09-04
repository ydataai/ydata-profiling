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
    Unsupported,
)


def test_summarizer():
    pps = PandasProfilingSummarizer()

    print(format_summary(pps.summarize(pd.Series([1, 2, 3, 4, 5]), Unsupported)))
    print(format_summary(pps.summarize(pd.Series([1, 2, 3, 4, 5]), Numeric)))
    print(
        format_summary(
            pps.summarize(
                pd.Series(pd.date_range(start="1/1/2018", end="1/08/2018")), DateTime
            )
        )
    )
    print(format_summary(pps.summarize(pd.Series(["abc", "abc", "abba"]), Categorical)))
    print(format_summary(pps.summarize(pd.Series(["https://www.example.com"]), URL)))
    print(
        format_summary(
            pps.summarize(
                pd.Series(
                    [
                        r"C:\Users\Cees Closed\Documents\code\pandas-profiling\src\pandas_profiling\model\typeset.py"
                    ]
                ),
                Path,
            )
        )
    )
    print(
        format_summary(
            pps.summarize(
                pd.Series(
                    [
                        r"C:\Users\Cees Closed\Documents\code\pandas-profiling\src\pandas_profiling\model\typeset.py"
                    ]
                ),
                File,
            )
        )
    )
    print(
        format_summary(
            pps.summarize(
                pd.Series(
                    [
                        r"C:\Users\Cees Closed\Documents\code\pandas-profiling\docsrc\assets\lambda-labs.png"
                    ]
                ),
                Image,
            )
        )
    )
    print(
        format_summary(
            pps.summarize(pd.Series([True, False, True, False, False]), Boolean)
        )
    )
