"""Tests the include_index argument."""
import pandas as pd
import json
from pandas_profiling import ProfileReport

INDEX_COL = 'b'

df = pd.DataFrame({'a': [1, 2, 3], INDEX_COL: [10, 11, 12]})
df = df.set_index(INDEX_COL)


def test_drop_index_true_explicit():
    """Confirm the index is dropped when include_index is set to True."""
    profile = ProfileReport(df, include_index=True, progress_bar=False)
    profile_dict = json.loads(profile.to_json())

    assert INDEX_COL in profile_dict['variables'].keys()


def test_drop_index_true_implicit():
    """Confirm the index is dropped when include_index is not set."""
    profile = ProfileReport(df, progress_bar=False)
    profile_dict = json.loads(profile.to_json())

    assert INDEX_COL in profile_dict['variables'].keys()


def test_drop_index_false():
    """Confirm the index is dropped when include_index is set to False."""
    profile = ProfileReport(df, include_index=False, progress_bar=False)
    profile_dict = json.loads(profile.to_json())

    assert INDEX_COL not in profile_dict['variables'].keys()
