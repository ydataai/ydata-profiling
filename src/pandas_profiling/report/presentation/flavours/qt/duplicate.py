from pandas_profiling.report.presentation.core import Duplicate
from PyQt5.QtWidgets import QPushButton


class QtDuplicate(Duplicate):
    def render(self):
        return QPushButton(self.content["name"])
