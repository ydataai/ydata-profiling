"""Logic for alerting the user on possibly problematic patterns in the data (e.g. high number of zeros , constant
values, high correlations)."""
from enum import Enum, auto, unique
from typing import Any, Dict, List, Optional, Set, Union

import numpy as np
import pandas as pd

from pandas_profiling.config import Settings
from pandas_profiling.model.correlations import perform_check_correlation


@unique
class AlertType(Enum):
    """Alert types"""

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


class Alert:
    """An alert object (type, values, column)."""

    _anchor_id: Optional[str] = None

    def __init__(
        self,
        alert_type: AlertType,
        values: Optional[Dict] = None,
        column_name: Union[str, None] = None,
        fields: Optional[Set] = None,
    ):
        if values is None:
            values = {}
        if fields is None:
            fields = set()

        self.fields = fields
        self.alert_type = alert_type
        self.values = values
        self.column_name = column_name

    @property
    def anchor_id(self) -> Optional[str]:
        if self._anchor_id is None:
            self._anchor_id = str(hash(self.column_name))
        return self._anchor_id

    def fmt(self) -> str:
        # TODO: render in template
        name = self.alert_type.name.replace("_", " ")
        if name == "HIGH CORRELATION":
            num = len(self.values["fields"])
            title = ", ".join(self.values["fields"])
            name = f'<abbr title="This variable has a high correlation with {num} fields: {title}">HIGH CORRELATION</abbr>'
        return name

    def __repr__(self):
        alert_type = self.alert_type.name
        column = self.column_name
        return f"[{alert_type}] alert on column {column}"


def check_table_alerts(table: dict) -> List[Alert]:
    """Checks the overall dataset for alerts.

    Args:
        table: Overall dataset statistics.

    Returns:
        A list of alerts.
    """
    alerts = []
    if alert_value(table.get("n_duplicates", np.nan)):
        alerts.append(
            Alert(
                alert_type=AlertType.DUPLICATES,
                values=table,
                fields={"n_duplicates"},
            )
        )
    if table["n"] == 0:
        alerts.append(
            Alert(
                alert_type=AlertType.EMPTY,
                values=table,
                fields={"n"},
            )
        )
    return alerts


def numeric_alerts(config: Settings, summary: dict) -> List[Alert]:
    alerts = []

    # Skewness
    if skewness_alert(summary["skewness"], config.vars.num.skewness_threshold):
        alerts.append(
            Alert(
                alert_type=AlertType.SKEWED,
                fields={"skewness"},
            )
        )

    # Infinite values
    if alert_value(summary["p_infinite"]):
        alerts.append(
            Alert(
                alert_type=AlertType.INFINITE,
                fields={"p_infinite", "n_infinite"},
            )
        )

    # Zeros
    if alert_value(summary["p_zeros"]):
        alerts.append(
            Alert(
                alert_type=AlertType.ZEROS,
                fields={"n_zeros", "p_zeros"},
            )
        )

    if (
        "chi_squared" in summary
        and summary["chi_squared"]["pvalue"] > config.vars.num.chi_squared_threshold
    ):
        alerts.append(Alert(alert_type=AlertType.UNIFORM))

    return alerts


def categorical_alerts(config: Settings, summary: dict) -> List[Alert]:
    alerts = []

    # High cardinality
    if summary.get("n_distinct", np.nan) > config.vars.cat.cardinality_threshold:
        alerts.append(
            Alert(
                alert_type=AlertType.HIGH_CARDINALITY,
                fields={"n_distinct"},
            )
        )

    if (
        "chi_squared" in summary
        and summary["chi_squared"]["pvalue"] > config.vars.cat.chi_squared_threshold
    ):
        alerts.append(Alert(alert_type=AlertType.UNIFORM))

    if summary.get("date_warning"):
        alerts.append(Alert(alert_type=AlertType.TYPE_DATE))

    # Constant length
    if "composition" in summary and summary["min_length"] == summary["max_length"]:
        alerts.append(
            Alert(
                alert_type=AlertType.CONSTANT_LENGTH,
                fields={"composition_min_length", "composition_max_length"},
            )
        )

    return alerts


def generic_alerts(summary: dict) -> List[Alert]:
    alerts = []

    # Missing
    if alert_value(summary["p_missing"]):
        alerts.append(
            Alert(
                alert_type=AlertType.MISSING,
                fields={"p_missing", "n_missing"},
            )
        )

    return alerts


def supported_alerts(summary: dict) -> List[Alert]:
    alerts = []

    if summary.get("n_distinct", np.nan) == summary["n"]:
        alerts.append(
            Alert(
                alert_type=AlertType.UNIQUE,
                fields={"n_distinct", "p_distinct", "n_unique", "p_unique"},
            )
        )
    if summary.get("n_distinct", np.nan) == 1:
        summary["mode"] = summary["value_counts_without_nan"].index[0]
        alerts.append(
            Alert(
                alert_type=AlertType.CONSTANT,
                fields={"n_distinct"},
            )
        )
        alerts.append(
            Alert(
                alert_type=AlertType.REJECTED,
                fields=set(),
            )
        )
    return alerts


def unsupported_alerts(summary: Dict[str, Any]) -> List[Alert]:
    alerts = [
        Alert(
            alert_type=AlertType.UNSUPPORTED,
            fields=set(),
        ),
        Alert(
            alert_type=AlertType.REJECTED,
            fields=set(),
        ),
    ]
    return alerts


def check_variable_alerts(config: Settings, col: str, description: dict) -> List[Alert]:
    """Checks individual variables for alerts.

    Args:
        col: The column name that is checked.
        description: The series description.

    Returns:
        A list of alerts.
    """
    alerts = []

    alerts += generic_alerts(description)

    if description["type"] == "Unsupported":
        alerts += unsupported_alerts(description)
    else:
        alerts += supported_alerts(description)

        if description["type"] == "Categorical":
            alerts += categorical_alerts(config, description)
        if description["type"] == "Numeric":
            alerts += numeric_alerts(config, description)

    for idx in range(len(alerts)):
        alerts[idx].column_name = col
        alerts[idx].values = description
    return alerts


def check_correlation_alerts(config: Settings, correlations: dict) -> List[Alert]:
    alerts = []

    for corr, matrix in correlations.items():
        if config.correlations[corr].warn_high_correlations:
            threshold = config.correlations[corr].threshold
            correlated_mapping = perform_check_correlation(matrix, threshold)
            if len(correlated_mapping) > 0:
                for k, v in correlated_mapping.items():
                    alerts.append(
                        Alert(
                            column_name=k,
                            alert_type=AlertType.HIGH_CORRELATION,
                            values={"corr": corr, "fields": v},
                        )
                    )
    return alerts


def get_alerts(
    config: Settings, table_stats: dict, series_description: dict, correlations: dict
) -> List[Alert]:
    alerts = check_table_alerts(table_stats)
    for col, description in series_description.items():
        alerts += check_variable_alerts(config, col, description)
    alerts += check_correlation_alerts(config, correlations)
    alerts.sort(key=lambda alert: str(alert.alert_type))
    return alerts


def alert_value(value: float) -> bool:
    return not np.isnan(value) and value > 0.01


def skewness_alert(v: float, threshold: int) -> bool:
    return not np.isnan(v) and (v < (-1 * threshold) or v > threshold)


def type_date_alert(series: pd.Series) -> bool:
    from dateutil.parser import ParserError, parse

    try:
        series.apply(parse)
        return True
    except ParserError:
        return False
