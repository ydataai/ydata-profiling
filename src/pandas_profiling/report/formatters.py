"""Formatters are mappings from object(s) to a string."""
from typing import Dict, Callable

from jinja2.utils import escape
import numpy as np


def fmt_color(text: str, color: str) -> str:
    """Format a string in a certain color (`<span>`).

    Args:
      text: The text to format.
      color: Any valid CSS color.

    Returns:
        A `<span>` that contains the colored text.
    """
    return f'<span style="color:{color}">{text}</span>'


def fmt_class(text: str, cls: str) -> str:
    """Format a string in a certain class (`<span>`).

    Args:
      text: The text to format.
      cls: The name of the class.

    Returns:
        A `<span>` with a class added.
    """
    return f'<span class="{cls}">{text}</span>'


def fmt_bytesize(num: float, suffix: str = "B") -> str:
    """Change a number of bytes in a human readable format.

    Args:
      num: number to format
      suffix: (Default value = 'B')

    Returns:
      The value formatted in human readable format (e.g. KiB).
    """
    for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
        if abs(num) < 1024.0:
            return f"{num:3.1f} {unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f} Yi{suffix}"


def fmt_percent(value: float, edge_cases: bool = True) -> str:
    """Format a ratio as a percentage.

    Args:
        edge_cases: Check for edge cases?
        value: The ratio.

    Returns:
        The percentage with 1 point precision.
    """
    if not (1.0 >= value >= 0.0):
        raise ValueError(f"Value '{value}' should be a ratio between 1 and 0.")
    if edge_cases and round(value, 3) == 0 and value > 0:
        return "< 0.1%"
    if edge_cases and round(value, 3) == 1 and value < 1:
        return "> 99.9%"

    return f"{value*100:2.1f}%"


def fmt_numeric(value: float, precision=10) -> str:
    """Format any numeric value.

    Args:
        value: The numeric value to format.
        precision: The numeric precision

    Returns:
        The numeric value with the given precision.
    """
    return "{{:.{precision}g}}".format(precision=precision).format(value)


def fmt_array(value: np.ndarray, threshold=np.nan) -> str:
    """Format numpy arrays.

    Args:
        value: Array to format.
        threshold: Threshold at which to show ellipsis

    Returns:
        The string representation of the numpy array.
    """
    with np.printoptions(threshold=3, edgeitems=threshold):
        value = str(value)

    return value


def fmt(value) -> str:
    """Format any value.

    Args:
        value: The value to format.

    Returns:
        The numeric formatting if the value is float or int, the string formatting otherwise.
    """
    if type(value) in [float, int]:
        return fmt_numeric(value)
    else:
        return str(escape(value))


def get_fmt_mapping() -> Dict[str, Callable]:
    """Get a mapping from formatter name to the function

    Returns: formatter mapping
    """
    return {
        "fmt_percent": fmt_percent,
        "fmt_bytesize": fmt_bytesize,
        "fmt_numeric": fmt_numeric,
        "fmt_array": fmt_array,
        "fmt": fmt,
        "raw": lambda x: x,
    }
