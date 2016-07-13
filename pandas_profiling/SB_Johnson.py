from scipy import optimize as spo
from scipy import stats as sps
import pandas as pd
import numpy as np

def _y_gen(xdata):
    """
    this is private u sneaky snek
    """
    return sps.norm.ppf((
        sps.rankdata(xdata, method='max') - 3.0 / 8.0
    ) / (len(xdata) + .25))

def _f_fit(xdata, gamma, delta, lam):
    """so is this wtheck mate"""
    return gamma + delta * np.log(xdata / lam + np.sqrt((xdata / lam) ** 2 + 1))

def get_j_params(x):
    """
    calculates parameters for johnson transformation
    :param x: input variable
    :type x: numeric, np.array like object

    :return params: the parameters for the johnson transform
    :type params: list of parameters in order: gamma, delta, lambda
    """
    if not isinstance(x, pd.Series):
        x = pd.Series(x)
    xdata = x.dropna()
    params = spo.curve_fit(_f_fit, xdata, ydata=_y_gen(xdata), p0=[-1, 0.5, 1])[0]
    #return dict(zip(['gamma', 'delta', 'lam'], params))
    return params

def j_xform(x):
    """
    Johnson transform
    :param x: input variable
    :type x: numeric, np.array-like object

    :return x': johnson transformed x
    :type x': numeric, np array
    """
    return _f_fit(x, *get_j_params(x)) # need .values() if switching to dict


if __name__ == '__main__':
    # these are just random inputs to make sure the function is working
    test_in = [np.arange(100), np.asarray([5, 10] * 5)]

    for t_i in test_in:
        print(get_j_params(t_i))
        print(j_xform(t_i))
        print(type(t_i))
