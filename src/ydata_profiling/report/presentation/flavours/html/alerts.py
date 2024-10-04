from ydata_profiling.report.presentation.core.alerts import Alerts
from ydata_profiling.report.presentation.flavours.html import templates
from ydata_profiling.utils.styles import get_alert_styles


class HTMLAlerts(Alerts):
    def render(self) -> str:
        styles = get_alert_styles()

        return templates.template("alerts.html").render(**self.content, styles=styles)
