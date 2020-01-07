from PyQt5.QtWidgets import QPushButton

from pandas_profiling.report.presentation.core.frequency_table_small import (
    FrequencyTableSmall,
)


class QtFrequencyTableSmall(FrequencyTableSmall):
    def render(self):
        return QPushButton("PyQt5 button")
