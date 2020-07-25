import numpy as np
import pandas as pd

from pandas_profiling.model.base import get_var_type
<<<<<<< HEAD
from pandas_profiling.model.typeset import Numeric
=======
>>>>>>> 2c6b5df5f37940035b9cb22b5338f61e612147a4


def test_numeric_with_inf():
    s = pd.Series([1, 2, 3, 6, np.inf])
<<<<<<< HEAD
    assert get_var_type(s)["type"] == Numeric
=======
    assert get_var_type(s)["type"].__name__ == "Numeric"
>>>>>>> 2c6b5df5f37940035b9cb22b5338f61e612147a4
