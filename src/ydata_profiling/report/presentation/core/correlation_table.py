from typing import Any

import pandas as pd

from ydata_profiling.report.presentation.core.item_renderer import ItemRenderer
from ydata_profiling.i18n import _


class CorrelationTable(ItemRenderer):
    def __init__(self, name: str, correlation_matrix: pd.DataFrame, **kwargs):
        super().__init__(
            "correlation_table",
            {"correlation_matrix": correlation_matrix},
            name=name,
            **kwargs
        )

    def __repr__(self) -> str:
        return _("core.correlationTable")

    def render(self) -> Any:
        raise NotImplementedError()
