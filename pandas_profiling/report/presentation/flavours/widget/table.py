from ipywidgets import widgets, GridspecLayout

from pandas_profiling.report.formatters import fmt
from pandas_profiling.report.presentation.core.table import Table


def get_table(items):
    table = GridspecLayout(len(items), 2)
    for row_id, item in enumerate(items):
        table[row_id, 0] = widgets.HTML(item["name"])
        table[row_id, 1] = widgets.HTML(fmt(item["value"]))

    return table


class WidgetTable(Table):
    def render(self):
        return get_table(self.content["rows"])
