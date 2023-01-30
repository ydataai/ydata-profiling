from abc import ABC
from typing import Optional

from ydata_profiling.report.presentation.core.renderable import Renderable


class ItemRenderer(Renderable, ABC):
    def __init__(
        self,
        item_type: str,
        content: dict,
        name: Optional[str] = None,
        anchor_id: Optional[str] = None,
        classes: Optional[str] = None,
    ):
        super().__init__(content, name, anchor_id, classes)
        self.item_type = item_type
