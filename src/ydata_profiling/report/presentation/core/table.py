from typing import Any, Optional, Sequence

from ydata_profiling.config import Style
from ydata_profiling.report.presentation.core.item_renderer import ItemRenderer
from ydata_profiling.i18n import _


class Table(ItemRenderer):
    def __init__(
        self,
        rows: Sequence,
        style: Style,
        name: Optional[str] = None,
        caption: Optional[str] = None,
        **kwargs
    ):
        super().__init__(
            "table",
            {"rows": rows, "name": name, "caption": caption, "style": style},
            **kwargs
        )

    def __repr__(self) -> str:
        return _("core.table")

    def render(self) -> Any:
        raise NotImplementedError()
