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
        HTMLPreview,
        HTMLOverview,
        HTMLTable,
        HTMLImage,
        HTMLHTML,
        HTMLFrequencyTable,
        HTMLFrequencyTableSmall,
        HTMLDataset,
        HTMLSample,
    )
    from pandas_profiling.report.presentation.core import (
        Sequence,
        Preview,
        Overview,
        Table,
        Image,
        HTML,
        FrequencyTable,
        FrequencyTableSmall,
        Dataset,
        Sample,
    )

    return {
        Sequence: HTMLSequence,
        Preview: HTMLPreview,
        Overview: HTMLOverview,
        Table: HTMLTable,
        HTML: HTMLHTML,
        Image: HTMLImage,
        FrequencyTable: HTMLFrequencyTable,
        FrequencyTableSmall: HTMLFrequencyTableSmall,
        Dataset: HTMLDataset,
        Sample: HTMLSample,
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
        WidgetPreview,
        WidgetOverview,
        WidgetTable,
        WidgetImage,
        WidgetHTML,
        WidgetFrequencyTable,
        WidgetFrequencyTableSmall,
        WidgetDataset,
        WidgetSample,
    )
    from pandas_profiling.report.presentation.core import (
        Sequence,
        Preview,
        Overview,
        Table,
        Image,
        HTML,
        FrequencyTable,
        FrequencyTableSmall,
        Dataset,
        Sample,
    )

    return {
        Sequence: WidgetSequence,
        Preview: WidgetPreview,
        Overview: WidgetOverview,
        Table: WidgetTable,
        HTML: WidgetHTML,
        Image: WidgetImage,
        FrequencyTable: WidgetFrequencyTable,
        FrequencyTableSmall: WidgetFrequencyTableSmall,
        Dataset: WidgetDataset,
        Sample: WidgetSample,
    }


def WidgetReport(structure: Renderable):
    mapping = get_html_renderable_mapping()
    apply_renderable_mapping(mapping, structure, flavour=WidgetReport)
    return structure


def get_qt_renderable_mapping() -> Dict[Type[Renderable], Type[Renderable]]:
    from pandas_profiling.report.presentation.flavours.qt import (
        QtSequence,
        QtPreview,
        QtOverview,
        QtTable,
        QtImage,
        QtHTML,
        QtFrequencyTable,
        QtFrequencyTableSmall,
        QtDataset,
        QtSample,
    )
    from pandas_profiling.report.presentation.core import (
        Sequence,
        Preview,
        Overview,
        Table,
        Image,
        HTML,
        FrequencyTable,
        FrequencyTableSmall,
        Dataset,
        Sample,
    )

    return {
        Sequence: QtSequence,
        Preview: QtPreview,
        Overview: QtOverview,
        Table: QtTable,
        HTML: QtHTML,
        Image: QtImage,
        FrequencyTable: QtFrequencyTable,
        FrequencyTableSmall: QtFrequencyTableSmall,
        Dataset: QtDataset,
        Sample: QtSample,
    }


def QtReport(structure: Renderable):
    mapping = get_qt_renderable_mapping()
    apply_renderable_mapping(mapping, structure, flavour=QtReport)
    return structure
