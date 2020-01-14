from typing import Dict, Type

from pandas_profiling.report.presentation.abstract.renderable import Renderable


def HTMLReport(structure: Renderable):
    """Adds HTML flavour to Renderable

    Args:
        structure:

    Returns:

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

    mapping: Dict[Type[Renderable], Type[Renderable]] = {
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

    for key, value in mapping.items():
        if isinstance(structure, key):
            value.convert_to_class(structure, HTMLReport)

    return structure


def WidgetReport(structure: Renderable):
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

    mapping: Dict[Type[Renderable], Type[Renderable]] = {
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

    for key, value in mapping.items():
        if isinstance(structure, key):
            value.convert_to_class(structure, WidgetReport)

    return structure


def QtReport(structure: Renderable):
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

    mapping: Dict[Type[Renderable], Type[Renderable]] = {
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

    for key, value in mapping.items():
        if isinstance(structure, key):
            value.convert_to_class(structure, QtReport)

    return structure
