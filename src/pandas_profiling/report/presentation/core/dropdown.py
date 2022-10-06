from typing import Any

from pandas_profiling.report.presentation.core.item_renderer import ItemRenderer


class Dropdown(ItemRenderer):
    def __init__(self, name: str, id: str, items: list, **kwargs):
        super().__init__("dropdown", {"name": name, "id": id, "items": items}, **kwargs)

    def __repr__(self) -> str:
        return "Dropdown"

    def render(self) -> Any:
        raise NotImplementedError()
