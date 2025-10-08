from typing import Any

from ydata_profiling.report.presentation.core.item_renderer import ItemRenderer
from ydata_profiling.i18n import _


class ToggleButton(ItemRenderer):
    def __init__(self, text: str, **kwargs):
        super().__init__("toggle_button", {"text": text}, **kwargs)

    def __repr__(self) -> str:
        return _("core.toggle_button")

    def render(self) -> Any:
        raise NotImplementedError()
