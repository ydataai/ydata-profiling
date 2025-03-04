"""
Test for issue 664:
https://github.com/ydataai/ydata-profiling/issues/664
"""
import numpy as np
import pandas as pd

from ydata_profiling import ProfileReport


def test_issue664():
    n = 10000
    df = pd.DataFrame({"a": [np.nan] * n, "b": ["b"] * n, "c": [pd.NaT] * n})
    df = df.fillna(value=np.nan)

    profile = ProfileReport(
        df, title="YData Profiling Report", explorative=True, minimal=True
    )
    _ = profile.get_description()


def test_issue664_alt():
    test = pd.DataFrame([np.nan] * 100, columns=["a"])

    profile = ProfileReport(test)
    assert len(profile.to_html()) > 0
