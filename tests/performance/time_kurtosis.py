import timeit

testcode = """
import numpy as np
import pandas as pd
import scipy.stats

np.random.seed(12)
vals = np.random.random(1000)
series = pd.Series(vals)
series[series < 0.2] = pd.NA

def f1(series):
    arr = series.values
    return scipy.stats.kurtosis(arr, bias=False, nan_policy='omit')


def f2(series):
    arr = series.values
    arr_without_nan = arr[~np.isnan(arr)]
    return scipy.stats.kurtosis(arr_without_nan, bias=False)


def f3(series):
    return series.kurtosis()


def f4(series):
    return series[series.notna()].kurtosis()
"""


print(timeit.timeit("f1(series)", number=10, setup=testcode))
print(timeit.timeit("f2(series)", number=10, setup=testcode))
print(timeit.timeit("f3(series)", number=10, setup=testcode))
print(timeit.timeit("f4(series)", number=10, setup=testcode))
