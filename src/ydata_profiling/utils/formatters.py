"""Basic formatting utility functions."""
from typing import Any, Callable

import numpy as np
import pandas as pd


def list_args(func: Callable) -> Callable:
    """Extend the function to allow taking a list as the first argument, and apply the function on each of the elements.

    Args:
        func: the function to extend

    Returns:
        The extended function
    """

    def inner(arg: Any, *args: Any, **kwargs: Any) -> Any:
        if isinstance(arg, list):
            return [func(v, *args, **kwargs) for v in arg]

        return func(arg, *args, **kwargs)

    return inner


@list_args
def fmt_percent(value: float, edge_cases: bool = True) -> str:
    """Format a ratio as a percentage.

    Args:
        edge_cases: Check for edge cases?
        value: The ratio.

    Returns:
        The percentage with 1 point precision.
    """
    if edge_cases and round(value, 3) == 0 and value > 0:
        return "< 0.1%"
    if edge_cases and round(value, 3) == 1 and value < 1:
        return "> 99.9%"

    return f"{value*100:2.1f}%"


@list_args
def fmt_numeric(value: float, precision: int = 10) -> str:
    """Format any numeric value.

    Args:
        value: The numeric value to format.
        precision: The numeric precision

    Returns:
        The numeric value with the given precision.
    """
    if value is None:
        fmtted = "N/A"
    else:
        fmtted = f"{{:.{precision}g}}".format(value)
        for v in ["e+", "e-"]:
            if v in fmtted:
                sign = "-" if v in "e-" else ""
                fmtted = fmtted.replace(v, " × 10<sup>") + "</sup>"
                fmtted = fmtted.replace("<sup>0", "<sup>")
                fmtted = fmtted.replace("<sup>", f"<sup>{sign}")

    return fmtted


@list_args
def fmt_number(value: int) -> str:
    """Format any numeric value.

    Args:
        value: The numeric value to format.

    Returns:
        The numeric value with the given precision.
    """
    return f"{value:n}"


@list_args
def fmt_array(value: np.ndarray, threshold: Any = np.nan) -> str:
    """Format numpy arrays.

    Args:
        value: Array to format.
        threshold: Threshold at which to show ellipsis

    Returns:
        The string representation of the numpy array.
    """
    with np.printoptions(threshold=3, edgeitems=threshold):
        return_value = str(value)

    return return_value
