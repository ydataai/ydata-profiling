from typing import Any

from pandas_profiling.report.presentation.abstract.item_renderer import ItemRenderer


class Report(ItemRenderer):
    """
    Wrapper for the report.
    """

    def __init__(self, name, body, footer, **kwargs):
        super().__init__(
            "report", {"body": body, "footer": footer}, name=name, **kwargs
        )

    def __repr__(self):
        return "Report"

    def render(self, **kwargs) -> Any:
        raise NotImplementedError()

    @classmethod
    def convert_to_class(cls, obj, flv) -> None:
        obj.__class__ = cls
        if "body" in obj.content:
            flv(obj.content["body"])
        if "footer" in obj.content:
            flv(obj.content["footer"])
