from PyQt5.QtWidgets import QPushButton

from pandas_profiling.report.presentation.core import ToggleButton


class QtToggleButton(ToggleButton):
    def render(self):
        return QPushButton("PyQt5 button")
