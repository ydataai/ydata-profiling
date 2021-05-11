"""Logic for alerting the user on possibly problematic patterns in the data (e.g. high number of zeros , constant
values, high correlations)."""
from enum import Enum, auto, unique
from typing import Any, Dict, List, Optional, Set, Union

import numpy as np
import pandas as pd

from pandas_profiling.config import Settings
from pandas_profiling.model.correlations import perform_check_correlation


@unique
class MessageType(Enum):
    """Message Types"""

    CONSTANT = auto()
    """This variable has a constant value."""

    ZEROS = auto()
    """This variable contains zeros."""

    HIGH_CORRELATION = auto()
    """This variable is highly correlated."""

    HIGH_CARDINALITY = auto()
    """This variable has a high cardinality."""

    UNSUPPORTED = auto()
    """This variable is unsupported."""

    DUPLICATES = auto()
    """This variable contains duplicates."""

    SKEWED = auto()
    """This variable is highly skewed."""

    MISSING = auto()
    """This variable contains missing values."""

    INFINITE = auto()
    """This variable contains infinite values."""

    TYPE_DATE = auto()
    """This variable is likely a datetime, but treated as categorical."""

    UNIQUE = auto()
    """This variable has unique values."""

    CONSTANT_LENGTH = auto()
    """This variable has a constant length"""

    REJECTED = auto()
    """Variables are rejected if we do not want to consider them for further analysis."""

    UNIFORM = auto()
    """The variable is uniformly distributed"""

    EMPTY = auto()
    """The DataFrame is empty"""


class Message:
    """A message object (type, values, column)."""

    _anchor_id: Optional[str] = None

    def __init__(
        self,
        message_type: MessageType,
        values: Optional[Dict] = None,
        column_name: Union[str, None] = None,
        fields: Optional[Set] = None,
    ):
        if values is None:
            values = {}
        if fields is None:
            fields = set()

        self.fields = fields
        self.message_type = message_type
        self.values = values
        self.column_name = column_name

    @property
    def anchor_id(self) -> Optional[str]:
        if self._anchor_id is None:
            self._anchor_id = str(hash(self.column_name))
        return self._anchor_id

    def fmt(self) -> str:
        # TODO: render in template
        name = self.message_type.name.replace("_", " ")
        if name == "HIGH CORRELATION":
            num = len(self.values["fields"])
            title = ", ".join(self.values["fields"])
            name = f'<abbr title="This variable has a high correlation with {num} fields: {title}">HIGH CORRELATION</abbr>'
        return name

    def __repr__(self):
        message_type = self.message_type.name
        column = self.column_name
        return f"[{message_type}] warning on column {column}"


def check_table_messages(table: dict) -> List[Message]:
    """Checks the overall dataset for warnings.

    Args:
        table: Overall dataset statistics.

    Returns:
        A list of messages.
    """
    messages = []
    if "n_duplicates" in table and warning_value(table["n_duplicates"]):
        messages.append(
            Message(
                message_type=MessageType.DUPLICATES,
                values=table,
                fields={"n_duplicates"},
            )
        )
    if table["n"] == 0:
        messages.append(
            Message(
                message_type=MessageType.EMPTY,
                values=table,
                fields={"n"},
            )
        )
    return messages


def numeric_warnings(config: Settings, summary: dict) -> List[Message]:
    messages = []

    chi_squared_threshold_num = config.vars.num.chi_squared_threshold

    # Skewness
    if warning_skewness(summary["skewness"], config.vars.num.skewness_threshold):
        messages.append(
            Message(
                message_type=MessageType.SKEWED,
                fields={"skewness"},
            )
        )

    # Infinite values
    if warning_value(summary["p_infinite"]):
        messages.append(
            Message(
                message_type=MessageType.INFINITE,
                fields={"p_infinite", "n_infinite"},
            )
        )

    # Zeros
    if warning_value(summary["p_zeros"]):
        messages.append(
            Message(
                message_type=MessageType.ZEROS,
                fields={"n_zeros", "p_zeros"},
            )
        )

    if (
        "chi_squared" in summary
        and summary["chi_squared"]["pvalue"] > chi_squared_threshold_num
    ):
        messages.append(Message(message_type=MessageType.UNIFORM))

    return messages


def categorical_warnings(config: Settings, summary: dict) -> List[Message]:
    messages = []

    cardinality_threshold_cat = config.vars.cat.cardinality_threshold
    chi_squared_threshold_cat = config.vars.cat.chi_squared_threshold

    # High cardinality
    if summary["n_distinct"] > cardinality_threshold_cat:
        messages.append(
            Message(
                message_type=MessageType.HIGH_CARDINALITY,
                fields={"n_distinct"},
            )
        )

    if (
        "chi_squared" in summary
        and summary["chi_squared"]["pvalue"] > chi_squared_threshold_cat
    ):
        messages.append(Message(message_type=MessageType.UNIFORM))

    if "date_warning" in summary and summary["date_warning"]:
        messages.append(Message(message_type=MessageType.TYPE_DATE))

    # Constant length
    if "composition" in summary and summary["min_length"] == summary["max_length"]:
        messages.append(
            Message(
                message_type=MessageType.CONSTANT_LENGTH,
                fields={"composition_min_length", "composition_max_length"},
            )
        )

    return messages


def generic_warnings(summary: dict) -> List[Message]:
    messages = []

    # Missing
    if warning_value(summary["p_missing"]):
        messages.append(
            Message(
                message_type=MessageType.MISSING,
                fields={"p_missing", "n_missing"},
            )
        )

    return messages


def supported_warnings(summary: dict) -> List[Message]:
    messages = []

    if summary["n_distinct"] == summary["n"]:
        messages.append(
            Message(
                message_type=MessageType.UNIQUE,
                fields={"n_distinct", "p_distinct", "n_unique", "p_unique"},
            )
        )
    if summary["n_distinct"] == 1:
        summary["mode"] = summary["value_counts_without_nan"].index[0]
        messages.append(
            Message(
                message_type=MessageType.CONSTANT,
                fields={"n_distinct"},
            )
        )
        messages.append(
            Message(
                message_type=MessageType.REJECTED,
                fields=set(),
            )
        )
    return messages


def unsupported_warnings(summary: Dict[str, Any]) -> List[Message]:
    messages = [
        Message(
            message_type=MessageType.UNSUPPORTED,
            fields=set(),
        ),
        Message(
            message_type=MessageType.REJECTED,
            fields=set(),
        ),
    ]
    return messages


def check_variable_messages(
    config: Settings, col: str, description: dict
) -> List[Message]:
    """Checks individual variables for warnings.

    Args:
        col: The column name that is checked.
        description: The series description.

    Returns:
        A list of messages.
    """
    messages = []

    messages += generic_warnings(description)

    if description["type"] == "Unsupported":
        messages += unsupported_warnings(description)
    else:
        messages += supported_warnings(description)

        if description["type"] == "Categorical":
            messages += categorical_warnings(config, description)
        if description["type"] == "Numeric":
            messages += numeric_warnings(config, description)

    for idx in range(len(messages)):
        messages[idx].column_name = col
        messages[idx].values = description
    return messages


def check_correlation_messages(config: Settings, correlations: dict) -> List[Message]:
    messages = []

    for corr, matrix in correlations.items():
        if config.correlations[corr].warn_high_correlations:
            threshold = config.correlations[corr].threshold
            correlated_mapping = perform_check_correlation(matrix, threshold)
            if len(correlated_mapping) > 0:
                for k, v in correlated_mapping.items():
                    messages.append(
                        Message(
                            column_name=k,
                            message_type=MessageType.HIGH_CORRELATION,
                            values={"corr": corr, "fields": v},
                        )
                    )
    return messages


def warning_value(value: float) -> bool:
    return not np.isnan(value) and value > 0.01


def warning_skewness(v: float, threshold: int) -> bool:
    return not np.isnan(v) and (v < (-1 * threshold) or v > threshold)


def warning_type_date(series: pd.Series) -> bool:
    from dateutil.parser import ParserError, parse

    try:
        series.apply(parse)
        return True
    except ParserError:
        return False
