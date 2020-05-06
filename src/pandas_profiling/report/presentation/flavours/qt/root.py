from pandas_profiling.report.presentation.core.root import Root
from PyQt5.QtWidgets import QPushButton


class QtRoot(Root):
    def render(self, **kwargs):
        return QPushButton("Root")
