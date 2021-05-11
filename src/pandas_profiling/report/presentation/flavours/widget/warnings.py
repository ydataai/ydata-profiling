from typing import List

from ipywidgets import HTML, Button, widgets

from pandas_profiling.report.presentation.core import Warnings
from pandas_profiling.report.presentation.flavours.html import templates


def get_row(items: List[widgets.Widget]) -> widgets.GridBox:
    layout = widgets.Layout(width="100%", grid_template_columns="75% 25%")
    return widgets.GridBox(items, layout=layout)


class WidgetWarnings(Warnings):
    def render(self) -> widgets.GridBox:
        styles = {
            "constant": "warning",
            "unsupported": "warning",
            "type_date": "warning",
            "high_cardinality": "danger",
            "unique": "danger",
            "uniform": "danger",
            "infinite": "info",
            "zeros": "info",
            "truncated": "info",
            "missing": "info",
            "skewed": "info",
            "high_correlation": "",
            "duplicates": "",
            "empty": "",
        }

        items = []
        for message in self.content["warnings"]:
            type_name = message.message_type.name.lower()
            if type_name == "rejected":
                continue

            items.append(
                HTML(
                    templates.template(f"warnings/warning_{type_name}.html").render(
                        message=message
                    )
                )
            )
            items.append(
                Button(
                    description=type_name.replace("_", " ").capitalize(),
                    button_style=styles[type_name],
                    disabled=True,
                )
            )

        return get_row(items)
