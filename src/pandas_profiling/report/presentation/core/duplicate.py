from typing import Any

from pandas_profiling.report.presentation.core.item_renderer import ItemRenderer


class Duplicate(ItemRenderer):
    def __init__(self, name, duplicate, **kwargs):
        super().__init__("duplicate", {"duplicate": duplicate}, name=name, **kwargs)

    def __repr__(self):
        return "Duplicate"

    def render(self) -> Any:
        raise NotImplementedError()
