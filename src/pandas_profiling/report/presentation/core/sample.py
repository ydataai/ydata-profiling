from typing import Any

from pandas_profiling.report.presentation.abstract.item_renderer import ItemRenderer


class Sample(ItemRenderer):
    def __init__(self, name, sample, **kwargs):
        super().__init__("sample", {"sample": sample}, name=name, **kwargs)

    def __repr__(self):
        return "Sample"

    def render(self) -> Any:
        raise NotImplementedError()
