"""Logic for alerting the user on possibly problematic patterns in the data (e.g. high number of zeros , constant
values, high correlations)."""
from enum import Enum, unique
from typing import List, Union
import warnings
from contextlib import suppress
import re
from dateutil.parser import parse

import numpy as np

from pandas_profiling.config import config
from pandas_profiling.model.base import Variable


@unique
class MessageType(Enum):
    """Message Types"""

    CONST = 1
    """This variable has a constant value."""

    ZEROS = 2
    """This variable contains zeros."""

    CORR = 3
    """This variable is highly correlated."""

    RECODED = 4
    """This variable is correlated (categorical)."""

    HIGH_CARDINALITY = 5
    """This variable has a high cardinality."""

    UNSUPPORTED = 6
    """This variable is unsupported."""

    DUPLICATES = 7
    """This variable contains duplicates."""

    SKEWED = 8
    """This variable is highly skewed."""

    MISSING = 9
    """This variable contains missing values."""

    INFINITE = 10
    """This variable contains infinite values."""

    TYPE_DATE = 11
    """This variable is likely a datetime, but treated as categorical."""


class Message(object):
    """A message object (type, values, column)."""

    def __init__(
        self,
        message_type: MessageType,
        values: dict,
        column_name: Union[str, None] = None,
    ):
        self.message_type = message_type
        self.values = values
        self.column_name = column_name


def check_table_messages(table: dict) -> List[Message]:
    """Checks the overall dataset for warnings.

    Args:
        table: Overall dataset statistics.

    Returns:
        A list of messages.
    """
    messages = []
    if warning_value(table["n_duplicates"]):
        messages.append(Message(message_type=MessageType.DUPLICATES, values=table))
    return messages


def check_variable_messages(col: str, description: dict) -> List[Message]:
    """Checks individual variables for warnings.

    Args:
        col: The column name that is checked.
        description: The series description.

    Returns:
        A list of messages.
    """
    messages = []
    # Special types
    if description["type"] in {
        Variable.S_TYPE_UNSUPPORTED,
        Variable.S_TYPE_CORR,
        Variable.S_TYPE_CONST,
        Variable.S_TYPE_RECODED,
    }:
        messages.append(
            Message(
                column_name=col,
                message_type=MessageType[description["type"].value],
                values=description,
            )
        )

    if description["type"] in {Variable.TYPE_CAT, Variable.S_TYPE_UNIQUE}:
        if description["date_warning"]:
            messages.append(
                Message(column_name=col, message_type=MessageType.TYPE_DATE, values={})
            )

    if description["type"] in {Variable.TYPE_CAT, Variable.TYPE_BOOL}:
        # High cardinality
        if description["distinct_count"] > config["cardinality_threshold"].get(int):
            messages.append(
                Message(
                    column_name=col,
                    message_type=MessageType.HIGH_CARDINALITY,
                    values=description,
                )
            )

    if description["type"] in {Variable.TYPE_NUM}:
        # Skewness
        if warning_skewness(description["skewness"]):
            messages.append(
                Message(
                    column_name=col, message_type=MessageType.SKEWED, values=description
                )
            )
        # Zeros
        if warning_value(description["p_zeros"]):
            messages.append(
                Message(
                    column_name=col, message_type=MessageType.ZEROS, values=description
                )
            )

    if description["type"] not in {
        Variable.S_TYPE_UNSUPPORTED,
        Variable.S_TYPE_CORR,
        Variable.S_TYPE_CONST,
        Variable.S_TYPE_RECODED,
    }:
        # Missing
        if warning_value(description["p_missing"]):
            messages.append(
                Message(
                    column_name=col,
                    message_type=MessageType.MISSING,
                    values=description,
                )
            )
        # Infinite values
        if warning_value(description["p_infinite"]):
            messages.append(
                Message(
                    column_name=col,
                    message_type=MessageType.INFINITE,
                    values=description,
                )
            )

    return messages


def warning_value(value: float) -> bool:
    return not np.isnan(value) and value > 0.01


def warning_skewness(v: float) -> bool:
    return not np.isnan(v) and (
        v < -config["vars"]["num"]["skewness_threshold"].get(int)
        or v > config["vars"]["num"]["skewness_threshold"].get(int)
    )


def _date_parser(date_string):
    pattern = re.compile(r"[.\-:]")
    pieces = re.split(pattern, date_string)

    if len(pieces) < 3:
        raise ValueError("Must have at least year, month and date passed")

    return parse(date_string)


def warning_type_date(series):
    with suppress(ValueError):
        with suppress(TypeError):
            series.apply(_date_parser)
            return True

    return False
