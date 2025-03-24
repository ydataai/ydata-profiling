"""
    HTML flavour mapping
"""
from ydata_profiling.report.presentation.core import *
from ydata_profiling.report.presentation.flavours.html import *
from ydata_profiling.report.presentation.flavours.flavours import register_flavour

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
