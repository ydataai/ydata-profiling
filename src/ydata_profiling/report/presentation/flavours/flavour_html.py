"""
    HTML flavour mapping
"""
from ydata_profiling.report.presentation.core import (
    HTML,
    Alerts,
    Collapse,
    Container,
    CorrelationTable,
    Dropdown,
    Duplicate,
    FrequencyTable,
    FrequencyTableSmall,
    Image,
    Root,
    Sample,
    Scores,
    Table,
    ToggleButton,
    Variable,
    VariableInfo,
)
from ydata_profiling.report.presentation.flavours.flavours import register_flavour
from ydata_profiling.report.presentation.flavours.html import (
    HTMLHTML,
    HTMLAlerts,
    HTMLCollapse,
    HTMLContainer,
    HTMLCorrelationTable,
    HTMLDropdown,
    HTMLDuplicate,
    HTMLFrequencyTable,
    HTMLFrequencyTableSmall,
    HTMLImage,
    HTMLRoot,
    HTMLSample,
    HTMLScores,
    HTMLTable,
    HTMLToggleButton,
    HTMLVariable,
    HTMLVariableInfo,
)

html_mapping = {
    Container: HTMLContainer,
    Variable: HTMLVariable,
    VariableInfo: HTMLVariableInfo,
    Table: HTMLTable,
    HTML: HTMLHTML,
    Root: HTMLRoot,
    Image: HTMLImage,
    FrequencyTable: HTMLFrequencyTable,
    FrequencyTableSmall: HTMLFrequencyTableSmall,
    Alerts: HTMLAlerts,
    Duplicate: HTMLDuplicate,
    Dropdown: HTMLDropdown,
    Sample: HTMLSample,
    ToggleButton: HTMLToggleButton,
    Collapse: HTMLCollapse,
    CorrelationTable: HTMLCorrelationTable,
    Scores: HTMLScores,
}

register_flavour("html", html_mapping)
