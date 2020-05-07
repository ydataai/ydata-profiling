import timeit

testcode = """
import numpy as np
import pandas as pd

np.random.seed(12)
vals = np.random.random(10000)
series = pd.Series(vals)
series[series < 0.3] = np.nan
series[series < 0.2] = np.Inf



def f1(series):
    return len(series.loc[(~np.isfinite(series)) & series.notnull()])
    
    
def f2(series):
    return ((series == np.inf) | (series == -np.inf)).sum()
"""


print(timeit.timeit("f1(series)", number=10, setup=testcode))
print(timeit.timeit("f2(series)", number=10, setup=testcode))
