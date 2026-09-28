"""Core presentation component for Smart Insights."""

from typing import Any, Dict, List, Optional

from data_profiling.report.presentation.core.item_renderer import ItemRenderer


class SmartInsights(ItemRenderer):
    """Presentation item for Smart Insights (missingness patterns and outlier reports)."""

    def __init__(
        self,
        missingness_findings: Optional[List[Any]] = None,
        outlier_reports: Optional[Dict[str, Any]] = None,
        **kwargs,
    ):
        super().__init__(
            "smart_insights",
            {
                "missingness_findings": missingness_findings or [],
                "outlier_reports": outlier_reports or {},
            },
            **kwargs,
        )

    def __repr__(self) -> str:
        return "SmartInsights"

    def render(self) -> Any:
        raise NotImplementedError()
