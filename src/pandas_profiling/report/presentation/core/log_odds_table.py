from typing import Any

from pandas_profiling.report.presentation.core.item_renderer import ItemRenderer


class LogOddsTable(ItemRenderer):
    def __init__(self, rows: list, redact: bool, **kwargs):
        super().__init__("frequency_table", {"rows": rows, "redact": redact}, **kwargs)

    def __repr__(self) -> str:
        return "LogOddsTable"

    def render(self) -> Any:
        raise NotImplementedError()
