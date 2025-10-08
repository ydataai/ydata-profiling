from typing import Any

from ydata_profiling.report.presentation.core.item_renderer import ItemRenderer
from ydata_profiling.i18n import _


class HTML(ItemRenderer):
    def __init__(self, content: str, **kwargs):
        super().__init__("html", {"html": content}, **kwargs)

    def __repr__(self) -> str:
        return _("core.html")

    def render(self) -> Any:
        raise NotImplementedError()
