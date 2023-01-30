"""
Test for issue 100:
https://github.com/ydataai/ydata-profiling/issues/100
"""
import numpy as np
import pandas as pd

from ydata_profiling import ProfileReport


def test_issue100():
    df = pd.DataFrame(np.random.randint(0, 1000, size=(1000, 4)), columns=list("ABCD"))
    df[["B", "C"]] = df[["B", "C"]].astype("category")

    report = ProfileReport(
        df,
        pool_size=1,
        title="Dataset with <em>Numeric</em> Categories",
        samples={"head": 20},
        progress_bar=False,
    )
    assert report.description_set is not None
