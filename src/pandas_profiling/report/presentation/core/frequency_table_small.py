from typing import Any

from pandas_profiling.report.presentation.abstract.item_renderer import ItemRenderer


class FrequencyTableSmall(ItemRenderer):
    def __init__(self, content, **kwargs):
        super().__init__("frequency_table_small", content, **kwargs)

    def __repr__(self):
        return "FrequencyTableSmall"

    def render(self) -> Any:
        raise NotImplementedError()
