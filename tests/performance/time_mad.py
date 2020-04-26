import timeit

testcode = '''
import numpy as np
import pandas as pd

np.random.seed(12)
vals = np.random.random(1000)
series = pd.Series(vals)
series[series < 0.2] = pd.NA


def mad(arr):
    """ Median Absolute Deviation: a "Robust" version of standard deviation.
        Indices variabililty of the sample.
        https://en.wikipedia.org/wiki/Median_absolute_deviation 
    """
    arr = np.ma.array(arr).compressed() # should be faster to not use masked arrays.
    med = np.median(arr)
    return np.median(np.abs(arr - med))
    
    
def mad2(arr):
    """ Median Absolute Deviation: a "Robust" version of standard deviation.
        Indices variabililty of the sample.
        https://en.wikipedia.org/wiki/Median_absolute_deviation 
    """
    med = np.median(arr)
    return np.median(np.abs(arr - med))
    
    
def f1(series):
    arr = series.values
    arr_without_nan = arr[~np.isnan(arr)]
    return mad(arr_without_nan)
    
    
def f2(series):
    arr = series.values
    arr_without_nan = arr[~np.isnan(arr)]
    return mad(arr_without_nan)
    

def f3(series):
    return series.mad()


def f4(series):
    return series[series.notna()].mad()
'''


print(timeit.timeit("f1(series)", number=10, setup=testcode))
print(timeit.timeit("f2(series)", number=10, setup=testcode))
print(timeit.timeit("f3(series)", number=10, setup=testcode))
print(timeit.timeit("f4(series)", number=10, setup=testcode))
