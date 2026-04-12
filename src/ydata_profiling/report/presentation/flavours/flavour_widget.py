"""
    Flavour widget
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
    Table,
    ToggleButton,
    Variable,
    VariableInfo,
)
from ydata_profiling.report.presentation.flavours.flavours import register_flavour
from ydata_profiling.report.presentation.flavours.widget import (
    WidgetAlerts,
    WidgetCollapse,
    WidgetContainer,
    WidgetCorrelationTable,
    WidgetDropdown,
    WidgetDuplicate,
    WidgetFrequencyTable,
    WidgetFrequencyTableSmall,
    WidgetHTML,
    WidgetImage,
    WidgetRoot,
    WidgetSample,
    WidgetTable,
    WidgetToggleButton,
    WidgetVariable,
    WidgetVariableInfo,
)

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
