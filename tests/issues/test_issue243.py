"""
Test for issue 243:
https://github.com/ydataai/ydata-profiling/issues/243
"""
import pandas as pd

from ydata_profiling import ProfileReport


def test_issue243():
    df = pd.DataFrame(data=[[1, 2], [3, 4]], columns=["Col 1", "Col 2"])
    columns_before = df.columns
    _ = ProfileReport(df, progress_bar=False, pool_size=1).description_set
    assert df.columns.tolist() == columns_before.tolist()


def test_issue243_unnamed():
    df = pd.DataFrame(data=[[1, 2], [3, 4]])
    columns_before = df.columns
    _ = ProfileReport(df, progress_bar=False, pool_size=1).description_set
    assert df.columns.tolist() == list(map(str, columns_before.tolist()))
