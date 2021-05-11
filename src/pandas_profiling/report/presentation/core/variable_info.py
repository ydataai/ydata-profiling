from typing import Any, List

from pandas_profiling.model.messages import Message
from pandas_profiling.report.presentation.core.item_renderer import ItemRenderer


class VariableInfo(ItemRenderer):
    def __init__(
        self,
        anchor_id: str,
        var_name: str,
        var_type: str,
        warnings: List[Message],
        description: str,
        **kwargs
    ):
        super().__init__(
            "variable_info",
            {
                "anchor_id": anchor_id,
                "var_name": var_name,
                "description": description,
                "var_type": var_type,
                "warnings": warnings,
            },
            **kwargs
        )

    def __repr__(self) -> str:
        return "VariableInfo"

    def render(self) -> Any:
        raise NotImplementedError()
