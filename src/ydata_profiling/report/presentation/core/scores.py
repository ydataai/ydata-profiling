"""
    Scores ItemRendered class
"""
from typing import Any, Dict, List, Optional

from ydata_profiling.config import Style
from ydata_profiling.report.presentation.core.item_renderer import ItemRenderer


class Scores(ItemRenderer):
    def __init__(
        self,
        items: List[Dict],
        overall_score: float,
        style: Style,
        name: Optional[str],
        **kwargs
    ):
        content = {
            "items": items,
            "overall_score": overall_score,
            "name": name,
            "style": style,
        }

        super().__init__("scores", content=content, **kwargs)

    def __repr__(self) -> str:
        return "Scores"

    def render(self) -> Any:
        raise NotImplementedError("Handled by flavour-specific class")
