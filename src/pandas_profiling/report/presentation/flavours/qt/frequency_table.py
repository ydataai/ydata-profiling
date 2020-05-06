from pandas_profiling.report.presentation.core import FrequencyTable
from PyQt5.QtWidgets import QPushButton


class QtFrequencyTable(FrequencyTable):
    def render(self):
        return QPushButton("Frequency Table")
