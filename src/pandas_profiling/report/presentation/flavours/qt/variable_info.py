from PyQt5.QtWidgets import QPushButton

from pandas_profiling.report.presentation.core import VariableInfo


class QtVariableInfo(VariableInfo):
    def render(self):
        return QPushButton("PyQt5 button")
