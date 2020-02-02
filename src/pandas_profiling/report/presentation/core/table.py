from typing import Any

from pandas_profiling.report.presentation.abstract.item_renderer import ItemRenderer


class Table(ItemRenderer):
    def __init__(self, rows, name=None, **kwargs):
        super().__init__("table", {"rows": rows, "name": name}, **kwargs)

    def render(self) -> Any:
        raise NotImplementedError()
