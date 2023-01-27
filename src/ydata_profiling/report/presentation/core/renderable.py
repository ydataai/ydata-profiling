from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, Optional


class Renderable(ABC):
    def __init__(
        self,
        content: Dict[str, Any],
        name: Optional[str] = None,
        anchor_id: Optional[str] = None,
        classes: Optional[str] = None,
    ):
        self.content = content
        if name is not None:
            self.content["name"] = name
        if anchor_id is not None:
            self.content["anchor_id"] = anchor_id
        if classes is not None:
            self.content["classes"] = classes

    @property
    def name(self) -> str:
        return self.content["name"]

    @property
    def anchor_id(self) -> str:
        return self.content["anchor_id"]

    @property
    def classes(self) -> str:
        return self.content["classes"]

    @abstractmethod
    def render(self) -> Any:
        pass

    def __str__(self):
        return self.__class__.__name__

    @classmethod
    def convert_to_class(cls, obj: "Renderable", flv: Callable) -> None:
        obj.__class__ = cls
