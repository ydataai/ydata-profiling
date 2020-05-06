from pandas_profiling.report.presentation.core import VariableInfo
from PyQt5.QtWidgets import QPushButton


class QtVariableInfo(VariableInfo):
    def render(self):
        return QPushButton("PyQt5 button")
