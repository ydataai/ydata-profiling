from collections import Counter

import numpy as np
import pandas as pd


def named_aggregate_summary_pandas(series: pd.Series, key: str):
    summary = {
        f"max_{key}": np.max(series),
        f"mean_{key}": np.mean(series),
        f"median_{key}": np.median(series),
        f"min_{key}": np.min(series),
    }

    return summary


def length_summary_pandas(series: pd.Series, summary: dict = {}) -> dict:
    # imported here to avoid circular imports
    from pandas_profiling.model.summary_helpers import named_aggregate_summary

    length = series.str.len()

    summary.update({"length": length})
    summary.update(named_aggregate_summary(length, "length"))

    return summary


def get_character_counts_pandas(series: pd.Series) -> Counter:
    """Function to return the character counts

    Args:
        series: the Series to process

    Returns:
        A dict with character counts
    """
    return Counter(series.str.cat())
