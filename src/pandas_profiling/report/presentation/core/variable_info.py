from typing import Any, List

from pandas_profiling.config import Style
from pandas_profiling.model.alerts import Alert
from pandas_profiling.report.presentation.core.item_renderer import ItemRenderer


class VariableInfo(ItemRenderer):
    def __init__(
        self,
        anchor_id: str,
        var_name: str,
        var_type: str,
        alerts: List[Alert],
        description: str,
        style: Style,
        **kwargs
    ):
        super().__init__(
            "variable_info",
            {
                "anchor_id": anchor_id,
                "var_name": var_name,
                "description": description,
                "var_type": var_type,
                "alerts": alerts,
                "style": style,
            },
            **kwargs
        )

    def __repr__(self) -> str:
        return "VariableInfo"

    def render(self) -> Any:
        raise NotImplementedError()
