from pandas_profiling.report.presentation.core import FrequencyTableSmall
from PyQt5.QtWidgets import QPushButton


class QtFrequencyTableSmall(FrequencyTableSmall):
    def render(self):
        return QPushButton("Small Frequency Table")
