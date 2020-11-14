"""
Test for issue 613:
https://github.com/pandas-profiling/pandas-profiling/issues/613
"""
import numpy as np
import pandas as pd

from pandas_profiling import ProfileReport

def test_issue100():

    df = pd.DataFrame([{'col': 'ABCD'}, {'col': 'DEFG'}, {'col': np.nan}])

    report = ProfileReport(df)
    
    assert report.description_set['variables']['col']['min_length'] = 0
    