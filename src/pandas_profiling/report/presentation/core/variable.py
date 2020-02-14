from typing import Union, Any

from pandas_profiling.report.presentation.abstract.item_renderer import ItemRenderer
from pandas_profiling.report.presentation.abstract.renderable import Renderable


class Variable(ItemRenderer):
    def __init__(
        self,
        top: Renderable,
        bottom: Union[Renderable, None] = None,
        ignore: bool = False,
        **kwargs
    ):
        super().__init__(
            "variable", {"top": top, "bottom": bottom, "ignore": ignore}, **kwargs
        )

    def __str__(self):
        text = "Variable\n"
        text += "- top: {}".format(str(self.content["top"]).replace("\n", "\n\t"))
        text += "- bottom: {}".format(str(self.content["bottom"]).replace("\n", "\n\t"))
        return text

    def __repr__(self):
        return "Variable"

    def render(self) -> Any:
        raise NotImplementedError()

    @classmethod
    def convert_to_class(cls, obj, flv):
        obj.__class__ = cls
        if "top" in obj.content and obj.content["top"] is not None:
            flv(obj.content["top"])
        if "bottom" in obj.content and obj.content["bottom"] is not None:
            flv(obj.content["bottom"])
