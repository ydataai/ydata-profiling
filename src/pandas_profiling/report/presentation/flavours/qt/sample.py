from pandas_profiling.report.presentation.core import Sample
from PyQt5.QtWidgets import QPushButton


class QtSample(Sample):
    def render(self):
        return QPushButton(self.content["name"])
