from typing import Any, Dict, List

from ipywidgets import GridspecLayout, VBox, widgets

from ydata_profiling.report.formatters import fmt_color
from ydata_profiling.report.presentation.core.table import Table


def get_table(items: List[Dict[str, Any]]) -> GridspecLayout:
    table = GridspecLayout(len(items), 2)
    for row_id, item in enumerate(items):
        name = item["name"]
        value = item["value"]
        if "alert" in item and item["alert"]:
            name = fmt_color(name, "var(--jp-error-color1)")
            value = fmt_color(value, "var(--jp-error-color1)")

        table[row_id, 0] = widgets.HTML(name)
        table[row_id, 1] = widgets.HTML(value)

    return table


class WidgetTable(Table):
    def render(self) -> VBox:
        items = [get_table(self.content["rows"])]
        if self.content["caption"] is not None:
            items.append(widgets.HTML(f'<em>{self.content["caption"]}</em>'))

        return VBox(items)
