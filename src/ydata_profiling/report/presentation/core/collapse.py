from typing import Any, Callable

from ydata_profiling.report.presentation.core.item_renderer import ItemRenderer
from ydata_profiling.report.presentation.core.renderable import Renderable
from ydata_profiling.report.presentation.core.toggle_button import ToggleButton


class Collapse(ItemRenderer):
    def __init__(self, button: ToggleButton, item: Renderable, **kwargs):
        super().__init__("collapse", {"button": button, "item": item}, **kwargs)

    def __repr__(self) -> str:
        return "Collapse"

    def render(self) -> Any:
        raise NotImplementedError()

    @classmethod
    def convert_to_class(cls, obj: Renderable, flv: Callable) -> None:
        obj.__class__ = cls
        if "button" in obj.content:
            flv(obj.content["button"])
        if "item" in obj.content:
            flv(obj.content["item"])
