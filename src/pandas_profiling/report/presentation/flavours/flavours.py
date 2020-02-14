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
        HTMLSequence,
        HTMLVariable,
        HTMLVariableInfo,
        HTMLTable,
        HTMLImage,
        HTMLHTML,
        HTMLFrequencyTable,
        HTMLFrequencyTableSmall,
        HTMLWarnings,
        HTMLSample,
        HTMLToggleButton,
        HTMLCollapse,
    )
    from pandas_profiling.report.presentation.core import (
        Sequence,
        Variable,
        VariableInfo,
        Table,
        Image,
        HTML,
        FrequencyTable,
        FrequencyTableSmall,
        Warnings,
        Sample,
        ToggleButton,
        Collapse,
    )

    return {
        Sequence: HTMLSequence,
        Variable: HTMLVariable,
        VariableInfo: HTMLVariableInfo,
        Table: HTMLTable,
        HTML: HTMLHTML,
        Image: HTMLImage,
        FrequencyTable: HTMLFrequencyTable,
        FrequencyTableSmall: HTMLFrequencyTableSmall,
        Warnings: HTMLWarnings,
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
        WidgetSequence,
        WidgetVariable,
        WidgetVariableInfo,
        WidgetTable,
        WidgetImage,
        WidgetHTML,
        WidgetFrequencyTable,
        WidgetFrequencyTableSmall,
        WidgetSample,
        WidgetWarnings,
        WidgetToggleButton,
        WidgetCollapse,
    )
    from pandas_profiling.report.presentation.core import (
        Sequence,
        Variable,
        VariableInfo,
        Table,
        Image,
        HTML,
        FrequencyTable,
        FrequencyTableSmall,
        Warnings,
        Sample,
        ToggleButton,
        Collapse,
    )

    return {
        Sequence: WidgetSequence,
        Variable: WidgetVariable,
        VariableInfo: WidgetVariableInfo,
        Table: WidgetTable,
        HTML: WidgetHTML,
        Image: WidgetImage,
        FrequencyTable: WidgetFrequencyTable,
        FrequencyTableSmall: WidgetFrequencyTableSmall,
        Warnings: WidgetWarnings,
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
        QtSequence,
        QtVariable,
        QtVariableInfo,
        QtTable,
        QtImage,
        QtHTML,
        QtFrequencyTable,
        QtFrequencyTableSmall,
        QtWarnings,
        QtSample,
        QtCollapse,
        QtToggleButton,
    )
    from pandas_profiling.report.presentation.core import (
        Sequence,
        Variable,
        VariableInfo,
        Table,
        Image,
        HTML,
        FrequencyTable,
        FrequencyTableSmall,
        Warnings,
        Sample,
        Collapse,
        ToggleButton,
    )

    return {
        Sequence: QtSequence,
        Variable: QtVariable,
        VariableInfo: QtVariableInfo,
        Table: QtTable,
        HTML: QtHTML,
        Image: QtImage,
        FrequencyTable: QtFrequencyTable,
        FrequencyTableSmall: QtFrequencyTableSmall,
        Warnings: QtWarnings,
        Sample: QtSample,
        Collapse: QtCollapse,
        ToggleButton: QtToggleButton,
    }


def QtReport(structure: Renderable):
    mapping = get_qt_renderable_mapping()
    apply_renderable_mapping(mapping, structure, flavour=QtReport)
    return structure
