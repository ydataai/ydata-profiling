from typing import Any, List

from pandas_profiling.report.presentation.abstract.renderable import Renderable


class Sequence(Renderable):
    def __init__(self, items: List[Renderable], sequence_type: str, **kwargs):
        super().__init__({"items": items}, **kwargs)
        self.sequence_type = sequence_type

    def __str__(self) -> str:
        text = "Sequence\n"
        if "items" in self.content:
            for id, item in enumerate(self.content["items"]):
                text += "- {}: {}\n".format(id, str(item).replace("\n", "\n\t"))
        return text

    def __repr__(self) -> str:
        if "name" in self.content:
            return "Sequence(name={name})".format(name=self.content["name"])
        else:
            return "Sequence"

    def render(self) -> Any:
        raise NotImplementedError()

    @classmethod
    def convert_to_class(cls, obj, flv) -> None:
        obj.__class__ = cls
        if "items" in obj.content:
            for item in obj.content["items"]:
                flv(item)
