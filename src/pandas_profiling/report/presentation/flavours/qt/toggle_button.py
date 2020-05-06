from pandas_profiling.report.presentation.core import ToggleButton
from PyQt5.QtWidgets import QPushButton


class QtToggleButton(ToggleButton):
    def render(self):
        return QPushButton("PyQt5 button")
