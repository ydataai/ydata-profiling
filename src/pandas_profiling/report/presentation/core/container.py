from typing import Any, Callable, Optional, Sequence

from pandas_profiling.report.presentation.core.renderable import Renderable


class Container(Renderable):
    def __init__(
        self,
        items: Sequence[Renderable],
        sequence_type: str,
        nested: bool = False,
        name: Optional[str] = None,
        anchor_id: Optional[str] = None,
        classes: Optional[str] = None,
        **kwargs,
    ):
        args = {"items": items, "nested": nested}
        args.update(**kwargs)
        super().__init__(args, name, anchor_id, classes)
        self.sequence_type = sequence_type

    def __str__(self) -> str:
        text = "Container\n"
        if "items" in self.content:
            for id, item in enumerate(self.content["items"]):
                name = str(item).replace("\n", "\n\t")
                text += f"- {id}: {name}\n"
        return text

    def __repr__(self) -> str:
        if "name" in self.content:
            name = self.content["name"]
            return f"Container(name={name})"
        else:
            return "Container"

    def render(self) -> Any:
        raise NotImplementedError()

    @classmethod
    def convert_to_class(cls, obj: Renderable, flv: Callable) -> None:
        obj.__class__ = cls
        if "items" in obj.content:
            for item in obj.content["items"]:
                flv(item)
