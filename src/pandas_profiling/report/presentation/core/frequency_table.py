from typing import Any

from pandas_profiling.report.presentation.abstract.item_renderer import ItemRenderer


class FrequencyTable(ItemRenderer):
    def __init__(self, rows, **kwargs):
        super().__init__("frequency_table", {"rows": rows}, **kwargs)

    def __repr__(self):
        return "FrequencyTable"

    def render(self) -> Any:
        raise NotImplementedError()
