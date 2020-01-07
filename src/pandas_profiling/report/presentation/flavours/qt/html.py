from PyQt5.QtWidgets import QPushButton

from pandas_profiling.report.presentation.core.html import HTML


class QtHTML(HTML):
    def render(self):
        return QPushButton(self.content["html"])
