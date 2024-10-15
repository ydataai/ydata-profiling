from typing import List

from ipywidgets import HTML, Button, widgets

from ydata_profiling.report.presentation.core import Alerts
from ydata_profiling.report.presentation.flavours.html import templates
from ydata_profiling.utils.styles import get_alert_styles


def get_row(items: List[widgets.Widget]) -> widgets.GridBox:
    layout = widgets.Layout(width="100%", grid_template_columns="75% 25%")
    return widgets.GridBox(items, layout=layout)


class WidgetAlerts(Alerts):
    def render(self) -> widgets.GridBox:
        styles = get_alert_styles()

        items = []
        for alert in self.content["alerts"]:
            type_name = alert.alert_type.name.lower()
            if type_name == "rejected":
                continue

            items.append(
                HTML(
                    templates.template(f"alerts/alert_{type_name}.html").render(
                        alert=alert
                    )
                )
            )

            style_name = styles[type_name]
            if style_name not in ("primary", "success", "info", "warning", "danger"):
                style_name = ""

            items.append(
                Button(
                    description=type_name.replace("_", " ").capitalize(),
                    button_style=style_name,
                    disabled=True,
                )
            )

        return get_row(items)
