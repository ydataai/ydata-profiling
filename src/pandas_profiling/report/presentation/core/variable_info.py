from typing import Any

from pandas_profiling.report.presentation.core.item_renderer import ItemRenderer


class VariableInfo(ItemRenderer):
    def __init__(self, anchor_id, var_name, var_type, warnings, description, **kwargs):
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

    def __repr__(self):
        return "VariableInfo"

    def render(self) -> Any:
        raise NotImplementedError()
