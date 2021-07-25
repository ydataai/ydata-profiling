from typing import Any

from pandas_profiling.report.presentation.core.item_renderer import ItemRenderer


class PDF(ItemRenderer):
    def __init__(self, content, **kwargs):
        super().__init__("pdf", {"pdf": content}, **kwargs)

    def __repr__(self):
        return "PDF"

    def render(self) -> Any:
        raise NotImplementedError()
