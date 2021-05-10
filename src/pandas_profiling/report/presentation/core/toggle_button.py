from typing import Any

from pandas_profiling.report.presentation.core.item_renderer import ItemRenderer


class ToggleButton(ItemRenderer):
    def __init__(self, text: str, **kwargs):
        super().__init__("toggle_button", {"text": text}, **kwargs)

    def __repr__(self) -> str:
        return "ToggleButton"

    def render(self) -> Any:
        raise NotImplementedError()
