from typing import Callable, Dict, Type

from pandas_profiling.report.presentation.core import Root
from pandas_profiling.report.presentation.core.renderable import Renderable


def apply_renderable_mapping(
    mapping: Dict[Type[Renderable], Type[Renderable]],
    structure: Renderable,
    flavour: Callable,
) -> None:
    mapping[type(structure)].convert_to_class(structure, flavour)


def get_html_renderable_mapping() -> Dict[Type[Renderable], Type[Renderable]]:
    """Workaround variable type annotations not being supported in Python 3.5

    Returns:
        type annotated mapping dict
    """
    from pandas_profiling.report.presentation.core import (
        HTML,
        Collapse,
        Container,
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
        Warnings,
    )
    from pandas_profiling.report.presentation.flavours.html import (
        HTMLHTML,
        HTMLCollapse,
        HTMLContainer,
        HTMLDuplicate,
        HTMLFrequencyTable,
        HTMLFrequencyTableSmall,
        HTMLImage,
        HTMLRoot,
        HTMLSample,
        HTMLTable,
        HTMLToggleButton,
        HTMLVariable,
        HTMLVariableInfo,
        HTMLWarnings,
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


def HTMLReport(structure: Root) -> Root:
    """Adds HTML flavour to Renderable

    Args:
        structure:

    Returns:

    """
    mapping = get_html_renderable_mapping()
    apply_renderable_mapping(mapping, structure, flavour=HTMLReport)
    return structure


def get_widget_renderable_mapping() -> Dict[Type[Renderable], Type[Renderable]]:
    from pandas_profiling.report.presentation.core import (
        HTML,
        Collapse,
        Container,
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
        Warnings,
    )
    from pandas_profiling.report.presentation.flavours.widget import (
        WidgetCollapse,
        WidgetContainer,
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
        WidgetWarnings,
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


def WidgetReport(structure: Root) -> Root:
    mapping = get_widget_renderable_mapping()
    apply_renderable_mapping(mapping, structure, flavour=WidgetReport)
    return structure
