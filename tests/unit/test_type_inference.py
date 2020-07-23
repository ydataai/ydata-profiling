import numpy as np
import pandas as pd

from pandas_profiling.model.base import get_var_type


def test_numeric_with_inf():
    s = pd.Series([1, 2, 3, 6, np.inf])
    assert get_var_type(s)["type"].__name__ == "Numeric"
