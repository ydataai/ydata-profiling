"""Utility functions for (version) compatibility"""

from contextlib import contextmanager
from functools import lru_cache
from typing import Generator, Tuple

import pandas as pd


@lru_cache(maxsize=1)
def pandas_version_info() -> Tuple[int, ...]:
    """
    Get the Pandas version as a tuple of integers,
    akin to `sys.version_info` for the Python version.
    """
    return tuple(int(s) for s in pd.__version__.split("."))


@contextmanager
def optional_option_context(
    option_key: str, value: object
) -> Generator[None, None, None]:
    """
    A context manager that sets an option only if it is available in the
    current pandas version; otherwise, it is a no-op.
    """
    try:
        with pd.option_context(option_key, value):
            yield
    except pd.errors.OptionError:
        yield
