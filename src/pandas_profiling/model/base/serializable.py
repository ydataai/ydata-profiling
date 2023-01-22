from abc import ABC, abstractmethod
from typing import Any, Dict


class SerializableInterface(ABC):
    """Interface for all classes, that needs to be serialized"""

    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        raise NotImplementedError()
