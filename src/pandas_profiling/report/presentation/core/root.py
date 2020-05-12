from typing import Any

from pandas_profiling.report.presentation.core.item_renderer import ItemRenderer
from pandas_profiling.report.presentation.core.renderable import Renderable


class Root(ItemRenderer):
    """
    Wrapper for the report.
    """

    def __init__(self, name: str, body: Renderable, footer: Renderable, **kwargs):
        super().__init__(
            "report", {"body": body, "footer": footer}, name=name, **kwargs
        )

    def __repr__(self):
        return "Root"

    def render(self, **kwargs) -> Any:
        raise NotImplementedError()

    @classmethod
    def convert_to_class(cls, obj, flv) -> None:
        obj.__class__ = cls
        if "body" in obj.content:
            flv(obj.content["body"])
        if "footer" in obj.content:
            flv(obj.content["footer"])
