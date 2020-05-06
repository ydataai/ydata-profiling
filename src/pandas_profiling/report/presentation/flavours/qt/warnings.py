from pandas_profiling.report.presentation.core import Warnings
from PyQt5.QtWidgets import QPushButton


class QtWarnings(Warnings):
    def render(self):
        return QPushButton("PyQt5 button")
