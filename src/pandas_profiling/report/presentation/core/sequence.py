from typing import Any

from pandas_profiling.report.presentation.abstract.renderable import Renderable


class Sequence(Renderable):
    def __init__(self, items, sequence_type, **kwargs):
        super().__init__({"items": items}, **kwargs)
        self.sequence_type = sequence_type

    def __str__(self):
        text = "Sequence\n"
        if "items" in self.content:
            for id, item in enumerate(self.content["items"]):
                text += "- {}: {}\n".format(id, str(item).replace("\n", "\n\t"))
        return text

    def render(self) -> Any:
        raise NotImplementedError()

    @classmethod
    def convert_to_class(cls, obj, flv):
        obj.__class__ = cls
        if "items" in obj.content:
            for item in obj.content["items"]:
                flv(item)
