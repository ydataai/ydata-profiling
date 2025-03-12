import os

import pandas as pd

from ydata_profiling.model.summarizer import ProfilingSummarizer, format_summary
from ydata_profiling.model.typeset import ProfilingTypeSet

base_path = os.path.abspath(os.path.dirname(__file__))


def test_summarizer(config):
    pps = ProfilingSummarizer(typeset=ProfilingTypeSet(config))

    _ = format_summary(pps.summarize(config, pd.Series([1, 2, 3, 4, 5]), "Unsupported"))
    _ = format_summary(pps.summarize(config, pd.Series([1, 2, 3, 4, 5]), "Numeric"))
    _ = format_summary(
        pps.summarize(
            config,
            pd.Series(pd.date_range(start="1/1/2018", end="1/08/2018")),
            "DateTime",
        )
    )
    _ = format_summary(
        pps.summarize(config, pd.Series(["abc", "abc", "abba"]), "Categorical")
    )
    _ = format_summary(
        pps.summarize(config, pd.Series(["https://www.example.com"]), "URL")
    )
    _ = format_summary(
        pps.summarize(
            config,
            pd.Series(
                [
                    os.path.abspath(
                        base_path
                        + r"../../../src/ydata_profiling/model/typeset_does_not_exist.py"
                    )
                ]
            ),
            "Path",
        )
    )
    _ = format_summary(
        pps.summarize(
            config,
            pd.Series(
                [
                    os.path.abspath(
                        base_path + r"../../../src/ydata_profiling/model/typeset.py"
                    )
                ]
            ),
            "File",
        )
    )
    _ = format_summary(
        pps.summarize(
            config,
            pd.Series(
                [os.path.abspath(base_path + r"../../../docsrc/assets/logo_header.png")]
            ),
            "Image",
        )
    )
    _ = format_summary(
        pps.summarize(config, pd.Series([True, False, True, False, False]), "Boolean")
    )
