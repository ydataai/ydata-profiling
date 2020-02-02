from PyQt5.QtWidgets import QPushButton

from pandas_profiling.report.presentation.core.overview import Overview


class QtOverview(Overview):
    def render(self):
        return QPushButton("PyQt5 button")
