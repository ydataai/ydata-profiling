from abc import ABC

from pandas_profiling.report.presentation.core.renderable import Renderable


class ItemRenderer(Renderable, ABC):
    def __init__(self, item_type, content, name=None, anchor_id=None, classes=None):
        super().__init__(content, name, anchor_id, classes)
        self.item_type = item_type
