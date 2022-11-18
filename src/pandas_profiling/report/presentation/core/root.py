from typing import Any, Callable

from pandas_profiling.config import Style
from pandas_profiling.report.presentation.core.item_renderer import ItemRenderer
from pandas_profiling.report.presentation.core.renderable import Renderable


class Root(ItemRenderer):
    """
    Wrapper for the report.
    """

    def __init__(
        self, name: str, body: Renderable, footer: Renderable, style: Style, **kwargs
    ):
        super().__init__(
            "report",
            {"body": body, "footer": footer, "style": style},
            name=name,
            **kwargs
        )

    def __repr__(self) -> str:
        return "Root"

    def render(self, **kwargs) -> Any:
        raise NotImplementedError()

    @classmethod
    def convert_to_class(cls, obj: Renderable, flv: Callable) -> None:
        obj.__class__ = cls
        if "body" in obj.content:
            flv(obj.content["body"])
        if "footer" in obj.content:
            flv(obj.content["footer"])
