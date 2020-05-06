from pandas_profiling.report.presentation.core import HTML
from PyQt5.QtWidgets import QPushButton


class QtHTML(HTML):
    def render(self):
        return QPushButton(self.content["html"])
