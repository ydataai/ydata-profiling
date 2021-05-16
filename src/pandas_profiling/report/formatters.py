"""Formatters are mappings from object(s) to a string."""
import decimal
import math
import re
from datetime import timedelta
from typing import Any, Dict, List, Optional, Union

import numpy as np
from markupsafe import escape


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


def fmt_timespan(num_seconds: Any, detailed: bool = False, max_units: int = 3) -> str:
    # From the `humanfriendly` module (without additional dependency)
    # https://github.com/xolox/python-humanfriendly/
    # Author: Peter Odding <peter@peterodding.com>
    # URL: https://humanfriendly.readthedocs.io

    time_units: List[Dict[str, Any]] = [
        {
            "divider": 1e-9,
            "singular": "nanosecond",
            "plural": "nanoseconds",
            "abbreviations": ["ns"],
        },
        {
            "divider": 1e-6,
            "singular": "microsecond",
            "plural": "microseconds",
            "abbreviations": ["us"],
        },
        {
            "divider": 1e-3,
            "singular": "millisecond",
            "plural": "milliseconds",
            "abbreviations": ["ms"],
        },
        {
            "divider": 1,
            "singular": "second",
            "plural": "seconds",
            "abbreviations": ["s", "sec", "secs"],
        },
        {
            "divider": 60,
            "singular": "minute",
            "plural": "minutes",
            "abbreviations": ["m", "min", "mins"],
        },
        {
            "divider": 60 * 60,
            "singular": "hour",
            "plural": "hours",
            "abbreviations": ["h"],
        },
        {
            "divider": 60 * 60 * 24,
            "singular": "day",
            "plural": "days",
            "abbreviations": ["d"],
        },
        {
            "divider": 60 * 60 * 24 * 7,
            "singular": "week",
            "plural": "weeks",
            "abbreviations": ["w"],
        },
        {
            "divider": 60 * 60 * 24 * 7 * 52,
            "singular": "year",
            "plural": "years",
            "abbreviations": ["y"],
        },
    ]

    def round_number(count: Any, keep_width: bool = False) -> str:
        text = f"{float(count):.2f}"
        if not keep_width:
            text = re.sub("0+$", "", text)
            text = re.sub(r"\.$", "", text)
        return text

    def coerce_seconds(value: Union[timedelta, int, float]) -> float:
        if isinstance(value, timedelta):
            return value.total_seconds()
        return float(value)

    def concatenate(items: List[str]) -> str:
        items = list(items)
        if len(items) > 1:
            return ", ".join(items[:-1]) + " and " + items[-1]
        elif items:
            return items[0]
        else:
            return ""

    def pluralize(count: Any, singular: str, plural: Optional[str] = None) -> str:
        if not plural:
            plural = singular + "s"
        return f"{count} {singular if math.floor(float(count)) == 1 else plural}"

    num_seconds = coerce_seconds(num_seconds)
    if num_seconds < 60 and not detailed:
        # Fast path.
        return pluralize(round_number(num_seconds), "second")
    else:
        # Slow path.
        result = []
        num_seconds = decimal.Decimal(str(num_seconds))
        relevant_units = list(reversed(time_units[0 if detailed else 3 :]))
        for unit in relevant_units:
            # Extract the unit count from the remaining time.
            divider = decimal.Decimal(str(unit["divider"]))
            count = num_seconds / divider
            num_seconds %= divider
            # Round the unit count appropriately.
            if unit != relevant_units[-1]:
                # Integer rounding for all but the smallest unit.
                count = int(count)
            else:
                # Floating point rounding for the smallest unit.
                count = round_number(count)
            # Only include relevant units in the result.
            if count not in (0, "0"):
                result.append(pluralize(count, unit["singular"], unit["plural"]))
        if len(result) == 1:
            # A single count/unit combination.
            return result[0]
        else:
            if not detailed:
                # Remove `insignificant' data from the formatted timespan.
                result = result[:max_units]
            # Format the timespan in a readable way.
            return concatenate(result)


def fmt_numeric(value: float, precision: int = 10) -> str:
    """Format any numeric value.

    Args:
        value: The numeric value to format.
        precision: The numeric precision

    Returns:
        The numeric value with the given precision.
    """
    fmtted = f"{{:.{precision}g}}".format(value)
    for v in ["e+", "e-"]:
        if v in fmtted:
            sign = "-" if v in "e-" else ""
            fmtted = fmtted.replace(v, " × 10<sup>") + "</sup>"
            fmtted = fmtted.replace("<sup>0", "<sup>")
            fmtted = fmtted.replace("<sup>", f"<sup>{sign}")

    return fmtted


def fmt_number(value: int) -> str:
    """Format any numeric value.

    Args:
        value: The numeric value to format.

    Returns:
        The numeric value with the given precision.
    """
    return f"{value:n}"


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


def fmt(value: Any) -> str:
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


def fmt_monotonic(value: int) -> str:
    if value == 2:
        return "Strictly increasing"
    elif value == 1:
        return "Increasing"
    elif value == 0:
        return "Not monotonic"
    elif value == -1:
        return "Decreasing"
    elif value == -2:
        return "Strictly decreasing"
    else:
        raise ValueError("Value should be integer ranging from -2 to 2.")


def help(title: str, url: Optional[str] = None) -> str:
    """Creat help badge

    Args:
        title: help text
        url: url to open in new tab (optional)

    Returns:
        HTML formatted help badge
    """
    if url is not None:
        return f'<a title="{title}" href="{url}" target="_blank"><span class="badge pull-right" style="color:#fff;background-color:#337ab7;" title="{title}">?</span></a>'
    else:
        return f'<span class="badge pull-right" style="color:#fff;background-color:#337ab7;" title="{title}">?</span>'


def fmt_badge(value: str) -> str:
    return re.sub(r"\((\d+)\)", r'<span class="badge">\1</span>', value)
