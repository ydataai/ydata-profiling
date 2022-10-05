from typing import Any

from pandas_profiling.report.presentation.core.item_renderer import ItemRenderer


class InputBox(ItemRenderer):
    def __init__(self, placeholder: str, id: str, **kwargs):
        super().__init__("input", {"placeholder": placeholder, "id": id}, **kwargs)

    def __repr__(self) -> str:
        return "InputBox"

    def render(self) -> Any:
        raise NotImplementedError()
