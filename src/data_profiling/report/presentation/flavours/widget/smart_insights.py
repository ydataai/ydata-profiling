"""Widget flavour for SmartInsights presentation component."""

from typing import Any

from data_profiling.report.presentation.core.smart_insights import SmartInsights


class WidgetSmartInsights(SmartInsights):
    """Widget renderer for SmartInsights component."""

    def render(self) -> Any:
        """Render widget placeholder.

        Returns:
            None
        """
        return None
