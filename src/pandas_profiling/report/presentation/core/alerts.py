from typing import Any, List

from pandas_profiling.config import Style
from pandas_profiling.model.alerts import Alert
from pandas_profiling.report.presentation.core.item_renderer import ItemRenderer


class Alerts(ItemRenderer):
    def __init__(self, alerts: List[Alert], style: Style, **kwargs):
        super().__init__("alerts", {"alerts": alerts, "style": style}, **kwargs)

    def __repr__(self):
        return "Alerts"

    def render(self) -> Any:
        raise NotImplementedError()
