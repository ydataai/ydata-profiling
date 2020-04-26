import pandas as pd
import numpy as np

from pandas_profiling.model.base import get_var_type


def test_numeric_with_inf():
    s = pd.Series([1, 2, 3, 4, 5, 6, np.inf])
    print(get_var_type(s))
