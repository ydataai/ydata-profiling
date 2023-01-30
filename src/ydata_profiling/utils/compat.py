"""Utility functions for (version) compatibility"""
from functools import lru_cache
from typing import Tuple

import pandas as pd


@lru_cache(maxsize=1)
def pandas_version_info() -> Tuple[int, ...]:
    """
    Get the Pandas version as a tuple of integers,
    akin to `sys.version_info` for the Python version.
    """
    return tuple(int(s) for s in pd.__version__.split("."))
