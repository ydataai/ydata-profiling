from typing import Tuple

import numpy as np
import pandas as pd


def weighted_median(data: np.ndarray, weights: np.ndarray) -> int:
    """
    Args:
      data (list or numpy.array): data
      weights (list or numpy.array): weights
    """
    if not isinstance(data, np.ndarray):
        data = np.array(data)
    if not isinstance(weights, np.ndarray):
        weights = np.array(weights)

    s_data, s_weights = map(np.sort, [data, weights])
    midpoint = 0.5 * np.sum(s_weights)

    if s_weights[-1] > midpoint:
        w_median = data[weights == np.max(weights)][0]
    else:
        cs_weights = np.cumsum(s_weights)
        idx = np.where(cs_weights <= midpoint)[0][-1]
        if cs_weights[idx] == midpoint:
            w_median = np.mean(s_data[idx : idx + 2])
        else:
            w_median = s_data[idx + 1]
    return w_median


def get_period_and_frequency(index: pd.DatetimeIndex) -> Tuple[float, str]:
    delta = abs(np.diff(index)).mean()
    delta = pd.Timedelta(delta)
    if delta.days > 0:
        frequency = "Days"
        period = delta / pd.Timedelta(days=1)
    elif delta.seconds > 0:
        if delta.seconds >= 3600:
            frequency = "Hours"
            period = delta / pd.Timedelta(seconds=3600)
        elif delta.seconds >= 60:
            frequency = "Minutes"
            period = delta / pd.Timedelta(seconds=60)
        else:
            frequency = "Seconds"
            period = delta / pd.Timedelta(seconds=1)
    elif delta.microseconds > 0:
        frequency = "Microseconds"
        period = delta / pd.Timedelta(microseconds=1)
    else:
        frequency = "Nanoseconds"
        period = delta.nanoseconds / pd.Timedelta(nanoseconds=1)
    return period, frequency
