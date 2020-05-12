from typing import Any

from pandas_profiling.report.presentation.core.item_renderer import ItemRenderer


class Warnings(ItemRenderer):
    def __init__(self, warnings, **kwargs):
        super().__init__("warnings", {"warnings": warnings}, **kwargs)

    def __repr__(self):
        return "Warnings"

    def render(self) -> Any:
        raise NotImplementedError()
