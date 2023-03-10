"""Logic for alerting the user on possibly problematic patterns in the data (e.g. high number of zeros , constant
values, high correlations)."""
from enum import Enum, auto, unique
from typing import Any, Dict, List, Optional, Set, Union

import numpy as np
import pandas as pd
from pandas_profiling.config import Settings
from pandas_profiling.model.correlations import perform_check_correlation
from pandas_profiling.model.description_variable import (
    CatDescription,
    CatDescriptionSupervised,
)
from pandas_profiling.model.missing import MissingConfMatrix


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

    MISSING_CORRELATED_WITH_TARGET = auto()
    """This variable missing values are related to target variable."""

    LOW_LOG_ODDS_RATIO = auto()
    """This variable has low log odds ratio for some value."""

    HIGH_LOG_ODDS_RATIO = auto()
    """This variable has high log odds ratio for some value."""

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

    NON_STATIONARY = auto()
    """The variable is a non-stationary series."""

    SEASONAL = auto()
    """The variable is a seasonal time series."""

    EMPTY = auto()
    """The DataFrame is empty"""


class Alert:
    """An alert object (type, values, column)."""

    _anchor_id: Optional[str] = None

    def __init__(
        self,
        alert_type: AlertType,
        values: Optional[Dict] = None,
        column_name: Optional[str] = None,
        fields: Optional[Set] = None,
    ):
        """
        Args:
            alert_type (AlertType) : Type of alert.
            values (dict): values, we can use in render.
            column_name (str): Name of related column to alert.
            fields (set)
        """
        if values is None:
            values = {}
        if fields is None:
            fields = set()

        self.fields = fields
        self.alert_type = alert_type
        self.values = values
        self.column_name = column_name

    @property
    def alert_type_name(self) -> str:
        return self.alert_type.name.replace("_", " ").lower().title()

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
            corr = self.values["corr"]
            name = f'<abbr title="This variable has a high {corr} correlation with {num} fields: {title}">HIGH CORRELATION</abbr>'
        elif "LOG ODDS RATIO" in name:
            log_odds_val = self.values["log_odds_ratio"]
            cat = self.values["category"]
            side = "low" if log_odds_val < 0 else "high"
            name = f"<abbr title=\"This variable has {side} log2 odds ratio for '{cat}'\">{name}</abbr>"

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


def log_odds_ratio_alert(config: Settings, summary: dict) -> List[Alert]:
    """Get log odds ratio alerts. If some value has highly different target
    distribution than in whole population, return info alert.

    Args:
        config (Settings): Setting of report.
        summary (dict): Description of one variable.
    """
    alerts = []
    if "plot_description" not in summary.keys():
        return alerts

    _description: Union[CatDescriptionSupervised, CatDescription] = summary[
        "plot_description"
    ]
    if not isinstance(_description, CatDescriptionSupervised):
        return alerts
    threshold = config.alerts.log_odds_ratio_threshold
    for index, row in _description.log_odds.iterrows():
        _log_odds_ratio = row[_description.log_odds_col_name]
        if abs(_log_odds_ratio) > threshold:
            alerts.append(
                Alert(
                    alert_type=AlertType.HIGH_LOG_ODDS_RATIO
                    if _log_odds_ratio > 0
                    else AlertType.LOW_LOG_ODDS_RATIO,
                    values={
                        "category": row[_description.data_col_name],
                        "log_odds_ratio": _log_odds_ratio,
                    },
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

    alerts += log_odds_ratio_alert(config, summary)

    return alerts


def timeseries_alerts(config: Settings, summary: dict) -> List[Alert]:
    alerts = numeric_alerts(config, summary)

    if not summary["stationary"]:
        alerts.append(Alert(alert_type=AlertType.NON_STATIONARY))

    if summary["seasonal"]:
        alerts.append(Alert(alert_type=AlertType.SEASONAL))

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

    alerts += log_odds_ratio_alert(config, summary)

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
    alerts: List[Alert] = []

    alerts += generic_alerts(description)

    if description["type"] == "Unsupported":
        alerts += unsupported_alerts(description)
    else:
        alerts += supported_alerts(description)

        if description["type"] == "Categorical":
            alerts += categorical_alerts(config, description)
        if description["type"] == "Numeric":
            alerts += numeric_alerts(config, description)
        if description["type"] == "TimeSeries":
            alerts += timeseries_alerts(config, description)

    for idx in range(len(alerts)):
        alerts[idx].column_name = col
        alerts[idx].values.update(description)
    return alerts


def check_correlation_alerts(config: Settings, correlations: dict) -> List[Alert]:
    alerts = []

    correlations_consolidated = {}
    for corr, matrix in correlations.items():
        if config.correlations[corr].warn_high_correlations:
            threshold = config.correlations[corr].threshold
            correlated_mapping = perform_check_correlation(matrix, threshold)
            for col, fields in correlated_mapping.items():
                set(fields).update(set(correlated_mapping.get(col, [])))
                correlations_consolidated[col] = fields

    if len(correlations_consolidated) > 0:
        for col, fields in correlations_consolidated.items():
            alerts.append(
                Alert(
                    column_name=col,
                    alert_type=AlertType.HIGH_CORRELATION,
                    values={"corr": "overall", "fields": fields},
                )
            )
    return alerts


def check_missing_alerts(config: Settings, missing: dict):
    """Check alerts from missing module.
    - check if missing are depend on target
    """
    alerts = []
    if "target" in missing.keys():
        conf_lvl = config.alerts.missing_confidence_level
        col: str
        value: MissingConfMatrix
        for col, value in missing["target"].missing_target.items():
            if 1 - value.p_value > conf_lvl:
                alerts.append(
                    Alert(
                        column_name=col,
                        alert_type=AlertType.MISSING_CORRELATED_WITH_TARGET,
                        values={"confidence_lvl": conf_lvl},
                    )
                )
    return alerts


def get_alerts(
    config: Settings,
    table_stats: dict,
    series_description: dict,
    correlations: dict,
    missing: dict,
) -> List[Alert]:
    """Return alerts from description.

    Args:
        config (Setting): Report setting.
        table_stats (dict): Description of DataFrame statistic.
        series_description (dict): Description of variables.
        correlations (dict): Description of correlations
        missing (dict): description of missing values.
    """
    alerts = check_table_alerts(table_stats)
    for col, description in series_description.items():
        alerts += check_variable_alerts(config, col, description)
    alerts += check_correlation_alerts(config, correlations)
    alerts += check_missing_alerts(config, missing)
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
    except ParserError:
        return False
    else:
        return True
