from typing import Any

from ydata_profiling.report.presentation.core.item_renderer import ItemRenderer
from ydata_profiling.i18n import _


class FrequencyTable(ItemRenderer):
    def __init__(self, rows: list, redact: bool, **kwargs):
        super().__init__("frequency_table", {"rows": rows, "redact": redact}, **kwargs)

    def __repr__(self) -> str:
        return _("core.frequencyTable")

    def render(self) -> Any:
        raise NotImplementedError()
