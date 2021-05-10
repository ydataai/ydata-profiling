from typing import Any, Optional, Sequence

from pandas_profiling.report.presentation.core.item_renderer import ItemRenderer


class Table(ItemRenderer):
    def __init__(
        self,
        rows: Sequence,
        name: Optional[str] = None,
        caption: Optional[str] = None,
        **kwargs
    ):
        super().__init__(
            "table", {"rows": rows, "name": name, "caption": caption}, **kwargs
        )

    def __repr__(self) -> str:
        return "Table"

    def render(self) -> Any:
        raise NotImplementedError()
