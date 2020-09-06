"""Logic for alerting the user on possibly problematic patterns in the data (e.g. high number of zeros , constant
values, high correlations)."""
from enum import Enum, auto, unique
from typing import List, Union

import numpy as np

from pandas_profiling.config import config
from pandas_profiling.model.correlations import perform_check_correlation
from pandas_profiling.model.typeset import Categorical, DateTime, Numeric, Unsupported


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


class Message(object):
    """A message object (type, values, column)."""

    def __init__(
        self,
        message_type: MessageType,
        values: dict,
        column_name: Union[str, None] = None,
        fields=None,
    ):
        if fields is None:
            fields = set()

        self.fields = fields
        self.message_type = message_type
        self.values = values
        self.column_name = column_name
        self.anchor_id = hash(column_name)

    def fmt(self):
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
    if warning_value(table["n_duplicates"]):
        messages.append(
            Message(
                message_type=MessageType.DUPLICATES,
                values=table,
                fields={"n_duplicates"},
            )
        )
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

    # Missing
    if warning_value(description["p_missing"]):
        messages.append(
            Message(
                column_name=col,
                message_type=MessageType.MISSING,
                values=description,
                fields={"p_missing", "n_missing"},
            )
        )

    if description["type"] == Unsupported:
        messages.append(
            Message(
                column_name=col,
                message_type=MessageType.UNSUPPORTED,
                values=description,
                fields={},
            )
        )
    elif description["n_distinct"] <= 1:
        description["mode"] = description["value_counts_without_nan"].index[0]
        messages.append(
            Message(
                column_name=col,
                message_type=MessageType.CONSTANT,
                values=description,
                fields={"n_distinct"},
            )
        )

    if description["type"] == Unsupported or description["n_distinct"] <= 1:
        messages.append(
            Message(
                column_name=col,
                message_type=MessageType.REJECTED,
                values=description,
                fields={},
            )
        )
    elif description["n_distinct"] == description["n"]:
        messages.append(
            Message(
                column_name=col,
                message_type=MessageType.UNIQUE,
                values=description,
                fields={"n_distinct", "p_distinct", "n_unique", "p_unique"},
            )
        )
    elif description["type"] in [
        Numeric,
        Categorical,
        DateTime,
    ]:
        # Uniformity
        if description["type"] == Categorical:
            # High cardinality
            if description["n_distinct"] > config["vars"]["cat"][
                "cardinality_threshold"
            ].get(int):
                messages.append(
                    Message(
                        column_name=col,
                        message_type=MessageType.HIGH_CARDINALITY,
                        values=description,
                        fields={"n_distinct"},
                    )
                )

            chi_squared_threshold = config["vars"]["cat"]["chi_squared_threshold"].get(
                float
            )
        else:
            chi_squared_threshold = config["vars"]["num"]["chi_squared_threshold"].get(
                float
            )

        if (
            "chi_squared" in description
            and description["chi_squared"]["pvalue"] > chi_squared_threshold
        ):
            messages.append(
                Message(column_name=col, message_type=MessageType.UNIFORM, values={})
            )

    # Categorical
    if description["type"] == Categorical:
        if "date_warning" in description and description["date_warning"]:
            messages.append(
                Message(column_name=col, message_type=MessageType.TYPE_DATE, values={})
            )

        # Constant length
        if (
            "composition" in description
            and description["min_length"] == description["max_length"]
        ):
            messages.append(
                Message(
                    column_name=col,
                    message_type=MessageType.CONSTANT_LENGTH,
                    values=description,
                    fields={"composition_min_length", "composition_max_length"},
                )
            )

    # Numerical
    if description["type"] == Numeric:
        # Skewness
        if warning_skewness(description["skewness"]):
            messages.append(
                Message(
                    column_name=col,
                    message_type=MessageType.SKEWED,
                    values=description,
                    fields={"skewness"},
                )
            )

        # Infinite values
        if warning_value(description["p_infinite"]):
            messages.append(
                Message(
                    column_name=col,
                    message_type=MessageType.INFINITE,
                    values=description,
                    fields={"p_infinite", "n_infinite"},
                )
            )

        # Zeros
        if warning_value(description["p_zeros"]):
            messages.append(
                Message(
                    column_name=col,
                    message_type=MessageType.ZEROS,
                    values=description,
                    fields={"n_zeros", "p_zeros"},
                )
            )

    return messages


def check_correlation_messages(correlations):
    messages = []

    for corr, matrix in correlations.items():
        if config["correlations"][corr]["warn_high_correlations"].get(bool):
            threshold = config["correlations"][corr]["threshold"].get(float)
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


def warning_skewness(v: float) -> bool:
    return not np.isnan(v) and (
        v < -config["vars"]["num"]["skewness_threshold"].get(int)
        or v > config["vars"]["num"]["skewness_threshold"].get(int)
    )


def warning_type_date(series):
    from dateutil.parser import ParserError, parse

    try:
        series.apply(parse)
        return True
    except ParserError:
        return False
