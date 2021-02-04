"""
Test for issue 664:
https://github.com/pandas-profiling/pandas-profiling/issues/664
"""
import numpy as np
import pandas as pd

from pandas_profiling import ProfileReport


def test_issue664():
    test = pd.DataFrame([np.nan] * 100, columns=["a"])

    profile = ProfileReport(test)
    assert len(profile.to_html()) > 0
