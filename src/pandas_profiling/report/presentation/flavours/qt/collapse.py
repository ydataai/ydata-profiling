from pandas_profiling.report.presentation.core import Collapse
from PyQt5.QtWidgets import QPushButton


class QtCollapse(Collapse):
    def render(self):
        return QPushButton("PyQt5 button")
