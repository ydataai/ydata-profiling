from typing import Any

from pandas_profiling.report.presentation.core.item_renderer import ItemRenderer


class FrequencyTableSmall(ItemRenderer):
    def __init__(self, rows, redact, **kwargs):
        super().__init__(
            "frequency_table_small", {"rows": rows, "redact": redact}, **kwargs
        )

    def __repr__(self):
        return "FrequencyTableSmall"

    def render(self) -> Any:
        raise NotImplementedError()
