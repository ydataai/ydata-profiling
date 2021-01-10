import numpy as np
import pandas as pd

from pandas_profiling import ProfileReport


def test_issue664():
    n = 10000
    df = pd.DataFrame({"a": [np.NaN] * n, "b": ["b"] * n, "c": [pd.NaT] * n})
    df = df.fillna(value=np.nan)

    profile = ProfileReport(
        df, title="Pandas Profiling Report", explorative=True, minimal=True
    )
    _ = profile.get_description()
