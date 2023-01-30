from typing import Any, List

from ydata_profiling.report.presentation.core.item_renderer import ItemRenderer


class FrequencyTableSmall(ItemRenderer):
    def __init__(self, rows: List[Any], redact: bool, **kwargs):
        super().__init__(
            "frequency_table_small", {"rows": rows, "redact": redact}, **kwargs
        )

    def __repr__(self) -> str:
        return "FrequencyTableSmall"

    def render(self) -> Any:
        raise NotImplementedError()
