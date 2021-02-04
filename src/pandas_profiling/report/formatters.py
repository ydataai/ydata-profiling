"""Formatters are mappings from object(s) to a string."""
from typing import Callable, Dict

import numpy as np
from jinja2.utils import escape


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


def fmt_timespan(num_seconds, detailed=False, max_units=3):
    # From the `humanfriendly` module (without additional dependency)
    # https://github.com/xolox/python-humanfriendly/
    # Author: Peter Odding <peter@peterodding.com>
    # URL: https://humanfriendly.readthedocs.io

    import decimal
    import math
    import numbers
    import re
    from datetime import datetime, timedelta

    time_units = (
        dict(
            divider=1e-9,
            singular="nanosecond",
            plural="nanoseconds",
            abbreviations=["ns"],
        ),
        dict(
            divider=1e-6,
            singular="microsecond",
            plural="microseconds",
            abbreviations=["us"],
        ),
        dict(
            divider=1e-3,
            singular="millisecond",
            plural="milliseconds",
            abbreviations=["ms"],
        ),
        dict(
            divider=1,
            singular="second",
            plural="seconds",
            abbreviations=["s", "sec", "secs"],
        ),
        dict(
            divider=60,
            singular="minute",
            plural="minutes",
            abbreviations=["m", "min", "mins"],
        ),
        dict(divider=60 * 60, singular="hour", plural="hours", abbreviations=["h"]),
        dict(divider=60 * 60 * 24, singular="day", plural="days", abbreviations=["d"]),
        dict(
            divider=60 * 60 * 24 * 7,
            singular="week",
            plural="weeks",
            abbreviations=["w"],
        ),
        dict(
            divider=60 * 60 * 24 * 7 * 52,
            singular="year",
            plural="years",
            abbreviations=["y"],
        ),
    )

    def round_number(count, keep_width=False):
        text = "%.2f" % float(count)
        if not keep_width:
            text = re.sub("0+$", "", text)
            text = re.sub(r"\.$", "", text)
        return text

    def coerce_seconds(value):
        if isinstance(value, timedelta):
            return value.total_seconds()
        if not isinstance(value, numbers.Number):
            msg = "Failed to coerce value to number of seconds! (%r)"
            raise ValueError(format(msg, value))
        return value

    def concatenate(items):
        items = list(items)
        if len(items) > 1:
            return ", ".join(items[:-1]) + " and " + items[-1]
        elif items:
            return items[0]
        else:
            return ""

    def pluralize(count, singular, plural=None):
        if not plural:
            plural = singular + "s"
        return "{} {}".format(
            count, singular if math.floor(float(count)) == 1 else plural
        )

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


def fmt_numeric(value: float, precision=10) -> str:
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
            fmtted = fmtted.replace(v, " × 10<sup>") + "</sup>"
            fmtted = fmtted.replace("<sup>0", "<sup>")

    return fmtted


def fmt_number(value: int) -> str:
    """Format any numeric value.

    Args:
        value: The numeric value to format.

    Returns:
        The numeric value with the given precision.
    """
    return f"{value:n}"


def fmt_array(value: np.ndarray, threshold=np.nan) -> str:
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


def help(title, url=None) -> str:
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


def get_fmt_mapping() -> Dict[str, Callable]:
    """Get a mapping from formatter name to the function

    Returns: formatter mapping
    """
    return {
        "fmt_percent": fmt_percent,
        "fmt_bytesize": fmt_bytesize,
        "fmt_timespan": fmt_timespan,
        "fmt_numeric": fmt_numeric,
        "fmt_number": fmt_number,
        "fmt_array": fmt_array,
        "fmt": fmt,
        "raw": lambda x: x,
    }
