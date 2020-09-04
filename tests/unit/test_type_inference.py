import numpy as np
import pandas as pd

from pandas_profiling.model.summarizer import PandasProfilingSummarizer
from pandas_profiling.model.summary import describe_1d
from pandas_profiling.model.typeset import Numeric, ProfilingTypeSet


def test_numeric_with_inf():
    s = pd.Series([1, 2, 3, 6, np.inf])
    assert describe_1d(s, summarizer=PandasProfilingSummarizer(), typeset=ProfilingTypeSet())["type"] == Numeric