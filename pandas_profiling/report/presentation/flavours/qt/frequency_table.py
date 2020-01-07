from PyQt5.QtWidgets import QPushButton

from pandas_profiling.report.presentation.core.frequency_table import FrequencyTable


class QtFrequencyTable(FrequencyTable):
    def render(self):
        return QPushButton("PyQt5 button")
