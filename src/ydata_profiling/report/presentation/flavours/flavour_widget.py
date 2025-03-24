"""
    Flavour widget
"""
from ydata_profiling.report.presentation.core import (Container, Variable, VariableInfo, Table, HTML, Root, Image,
                                                      FrequencyTable, FrequencyTableSmall, Alerts, Duplicate, Dropdown,
                                                      Sample, ToggleButton, Collapse, CorrelationTable)
from ydata_profiling.report.presentation.flavours.widget import (WidgetTable, WidgetContainer, WidgetVariable, WidgetVariableInfo,
                                                                 WidgetHTML, WidgetRoot, WidgetImage, WidgetFrequencyTable, WidgetFrequencyTableSmall,
                                                                 WidgetAlerts, WidgetDuplicate, WidgetDropdown, WidgetSample, WidgetToggleButton,
                                                                 WidgetCollapse, WidgetCorrelationTable)
from ydata_profiling.report.presentation.flavours.flavours import register_flavour

widget_mapping = {
    Container: WidgetContainer,
    Variable: WidgetVariable,
    VariableInfo: WidgetVariableInfo,
    Table: WidgetTable,
    HTML: WidgetHTML,
    Root: WidgetRoot,
    Image: WidgetImage,
    FrequencyTable: WidgetFrequencyTable,
    FrequencyTableSmall: WidgetFrequencyTableSmall,
    Alerts: WidgetAlerts,
    Duplicate: WidgetDuplicate,
    Dropdown: WidgetDropdown,
    Sample: WidgetSample,
    ToggleButton: WidgetToggleButton,
    Collapse: WidgetCollapse,
    CorrelationTable: WidgetCorrelationTable,
}

register_flavour("widget", widget_mapping)