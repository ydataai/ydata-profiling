from abc import ABC, abstractmethod
from typing import Any


class Renderable(ABC):
    def __init__(self, content, name=None, anchor_id=None, classes=None):
        self.content = content
        if name is not None:
            self.content["name"] = name
        if anchor_id is not None:
            self.content["anchor_id"] = anchor_id
        if classes is not None:
            self.content["classes"] = classes

    @property
    def name(self):
        return self.content["name"]

    @property
    def anchor_id(self):
        return self.content["anchor_id"]

    @property
    def classes(self):
        return self.content["classes"]

    @abstractmethod
    def render(self) -> Any:
        pass

    def __str__(self):
        return self.__class__.__name__

    @classmethod
    def convert_to_class(cls, obj, flv):
        obj.__class__ = cls
