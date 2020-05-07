from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem

from pandas_profiling.report.formatters import fmt
from pandas_profiling.report.presentation.core import Table


def get_table(items):
    from PyQt5.QtWidgets import QHeaderView

    table = QTableWidget()

    table.setRowCount(len(items))
    table.setColumnCount(2)

    horizontal = table.horizontalHeader()
    horizontal.setSectionResizeMode(QHeaderView.Stretch)
    horizontal.setVisible(False)

    vertical = table.verticalHeader()
    vertical.setVisible(False)

    for row_id, item in enumerate(items):
        table.setItem(row_id, 0, QTableWidgetItem(item["name"]))
        table.setItem(row_id, 1, QTableWidgetItem(fmt(item["value"])))

    return table


class QtTable(Table):
    def render(self):
        return get_table(self.content["rows"])
