"""
Test for issue 671:
https://github.com/ydataai/ydata-profiling/issues/671
"""
import numpy as np
import pandas as pd

from ydata_profiling import ProfileReport


def test_issue671():
    test = pd.DataFrame([0, 5, 22, 32, 65, np.nan], columns=["a"])

    for i in range(0, 10):
        profile = ProfileReport(
            test,
            vars={"num": {"low_categorical_threshold": i}},
            progress_bar=False,
            pool_size=1,
        )
        assert len(profile.to_html()) > 0
