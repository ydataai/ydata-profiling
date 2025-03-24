"""
    HTML flavour mapping
"""
from ydata_profiling.report.presentation.core import (Container, Variable, VariableInfo, Table, HTML, Root, Image,
                                                      FrequencyTable, FrequencyTableSmall, Alerts, Duplicate,
                                                      Dropdown, Sample, ToggleButton, Collapse,
                                                      CorrelationTable, Scores)
from ydata_profiling.report.presentation.flavours.html import (HTMLContainer, HTMLVariable, HTMLVariableInfo,
                                                               HTMLTable, HTMLHTML, HTMLRoot, HTMLImage,
                                                               HTMLFrequencyTable, HTMLFrequencyTableSmall,
                                                               HTMLAlerts, HTMLDuplicate, HTMLDropdown, HTMLScores,
                                                               HTMLSample, HTMLToggleButton, HTMLCollapse, HTMLCorrelationTable)
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
