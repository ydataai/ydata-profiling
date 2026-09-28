"""HTML flavour for SmartInsights presentation component."""

from data_profiling.report.presentation.core.smart_insights import SmartInsights
from data_profiling.report.presentation.flavours.html import templates


class HTMLSmartInsights(SmartInsights):
    """HTML renderer for SmartInsights component."""

    def render(self) -> str:
        """Render the smart insights section using the Jinja2 template.

        Returns:
            Rendered HTML string.
        """
        return templates.template("smart_insights.html").render(**self.content)
