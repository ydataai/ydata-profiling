from typing import Any

from ydata_profiling.report.presentation.core.item_renderer import ItemRenderer


class HTML(ItemRenderer):
    def __init__(self, content: str, **kwargs):
        super().__init__("html", {"html": content}, **kwargs)

    def __repr__(self) -> str:
        return "HTML"

    def render(self) -> Any:
        raise NotImplementedError()
