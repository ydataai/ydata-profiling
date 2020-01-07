from typing import Any

from pandas_profiling.report.presentation.abstract.item_renderer import ItemRenderer


class HTML(ItemRenderer):
    def __init__(self, content, **kwargs):
        super().__init__("html", {"html": content}, **kwargs)

    def render(self) -> Any:
        raise NotImplementedError()
