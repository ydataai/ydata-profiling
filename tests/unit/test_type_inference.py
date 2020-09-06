# import numpy as np
# import pandas as pd
#
# from pandas_profiling.model.summary import describe_1d
# from pandas_profiling.model.typeset import Numeric
#
#
# def test_numeric_with_inf(summarizer, typeset):
#     s = pd.Series([1, 2, 3, 6, np.inf])
#     assert describe_1d(s, summarizer, typeset)["type"] == Numeric
