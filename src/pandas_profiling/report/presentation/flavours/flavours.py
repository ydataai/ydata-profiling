from typing import Dict, Type

from pandas_profiling.report.presentation.abstract.renderable import Renderable


def apply_renderable_mapping(mapping, structure, flavour):
    for key, value in mapping.items():
        if isinstance(structure, key):
            value.convert_to_class(structure, flavour)


def get_html_renderable_mapping() -> Dict[Type[Renderable], Type[Renderable]]:
    """Workaround variable type annotations not being supported in Python 3.5

    Returns:
        type annotated mapping dict
    """
    from pandas_profiling.report.presentation.flavours.html import (
        HTMLContainer,
        HTMLVariable,
        HTMLVariableInfo,
        HTMLTable,
        HTMLImage,
        HTMLRoot,
        HTMLHTML,
        HTMLFrequencyTable,
        HTMLFrequencyTableSmall,
        HTMLWarnings,
        HTMLDuplicate,
        HTMLSample,
        HTMLToggleButton,
        HTMLCollapse,
    )
    from pandas_profiling.report.presentation.core import (
        Container,
        Variable,
        VariableInfo,
        Table,
        Image,
        HTML,
        Root,
        FrequencyTable,
        FrequencyTableSmall,
        Warnings,
        Duplicate,
        Sample,
        ToggleButton,
        Collapse,
    )

    return {
        Container: HTMLContainer,
        Variable: HTMLVariable,
        VariableInfo: HTMLVariableInfo,
        Table: HTMLTable,
        HTML: HTMLHTML,
        Root: HTMLRoot,
        Image: HTMLImage,
        FrequencyTable: HTMLFrequencyTable,
        FrequencyTableSmall: HTMLFrequencyTableSmall,
        Warnings: HTMLWarnings,
        Duplicate: HTMLDuplicate,
        Sample: HTMLSample,
        ToggleButton: HTMLToggleButton,
        Collapse: HTMLCollapse,
    }


def HTMLReport(structure: Renderable):
    """Adds HTML flavour to Renderable

    Args:
        structure:

    Returns:

    """
    mapping = get_html_renderable_mapping()
    apply_renderable_mapping(mapping, structure, flavour=HTMLReport)
    return structure


def get_widget_renderable_mapping() -> Dict[Type[Renderable], Type[Renderable]]:
    from pandas_profiling.report.presentation.flavours.widget import (
        WidgetContainer,
        WidgetVariable,
        WidgetVariableInfo,
        WidgetTable,
        WidgetImage,
        WidgetHTML,
        WidgetRoot,
        WidgetFrequencyTable,
        WidgetFrequencyTableSmall,
        WidgetDuplicate,
        WidgetSample,
        WidgetWarnings,
        WidgetToggleButton,
        WidgetCollapse,
    )
    from pandas_profiling.report.presentation.core import (
        Container,
        Variable,
        VariableInfo,
        Table,
        Image,
        HTML,
        FrequencyTable,
        FrequencyTableSmall,
        Warnings,
        Duplicate,
        Sample,
        Root,
        ToggleButton,
        Collapse,
    )

    return {
        Container: WidgetContainer,
        Variable: WidgetVariable,
        VariableInfo: WidgetVariableInfo,
        Table: WidgetTable,
        HTML: WidgetHTML,
        Root: WidgetRoot,
        Image: WidgetImage,
        FrequencyTable: WidgetFrequencyTable,
        FrequencyTableSmall: WidgetFrequencyTableSmall,
        Warnings: WidgetWarnings,
        Duplicate: WidgetDuplicate,
        Sample: WidgetSample,
        ToggleButton: WidgetToggleButton,
        Collapse: WidgetCollapse,
    }


def WidgetReport(structure: Renderable):
    mapping = get_widget_renderable_mapping()
    apply_renderable_mapping(mapping, structure, flavour=WidgetReport)
    return structure


def get_qt_renderable_mapping() -> Dict[Type[Renderable], Type[Renderable]]:
    from pandas_profiling.report.presentation.flavours.qt import (
        QtContainer,
        QtVariable,
        QtVariableInfo,
        QtTable,
        QtImage,
        QtRoot,
        QtHTML,
        QtFrequencyTable,
        QtFrequencyTableSmall,
        QtWarnings,
        QtDuplicate,
        QtSample,
        QtCollapse,
        QtToggleButton,
    )
    from pandas_profiling.report.presentation.core import (
        Container,
        Variable,
        VariableInfo,
        Table,
        Image,
        HTML,
        FrequencyTable,
        FrequencyTableSmall,
        Warnings,
        Duplicate,
        Root,
        Sample,
        Collapse,
        ToggleButton,
    )

    return {
        Container: QtContainer,
        Variable: QtVariable,
        VariableInfo: QtVariableInfo,
        Table: QtTable,
        HTML: QtHTML,
        Root: QtRoot,
        Image: QtImage,
        FrequencyTable: QtFrequencyTable,
        FrequencyTableSmall: QtFrequencyTableSmall,
        Warnings: QtWarnings,
        Duplicate: QtDuplicate,
        Sample: QtSample,
        Collapse: QtCollapse,
        ToggleButton: QtToggleButton,
    }


def QtReport(structure: Renderable):
    mapping = get_qt_renderable_mapping()
    apply_renderable_mapping(mapping, structure, flavour=QtReport)
    return structure
