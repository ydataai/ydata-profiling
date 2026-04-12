from typing import Any, Callable

from ydata_profiling.report.presentation.core.container import Container
from ydata_profiling.report.presentation.core.item_renderer import ItemRenderer
from ydata_profiling.report.presentation.core.renderable import Renderable


class Dropdown(ItemRenderer):
    def __init__(
        self,
        name: str,
        id: str,
        items: list,
        item: Container,
        anchor_id: str,
        classes: list,
        is_row: bool,
        **kwargs
    ):
        super().__init__(
            "dropdown",
            {
                "name": name,
                "id": id,
                "items": items,
                "item": item,
                "anchor_id": anchor_id,
                "classes": " ".join(classes),
                "is_row": is_row,
            },
            **kwargs
        )

    def __repr__(self) -> str:
        return "Dropdown"

    def render(self) -> Any:
        raise NotImplementedError()

    @classmethod
    def convert_to_class(cls, obj: Renderable, flv: Callable) -> None:
        obj.__class__ = cls
        if "item" in obj.content:
            flv(obj.content["item"])
