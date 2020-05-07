from PyQt5.QtWidgets import QPushButton

from pandas_profiling.report.presentation.core import Warnings


class QtWarnings(Warnings):
    def render(self):
        return QPushButton("PyQt5 button")
