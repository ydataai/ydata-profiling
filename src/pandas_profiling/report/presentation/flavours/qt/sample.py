from PyQt5.QtWidgets import QPushButton

from pandas_profiling.report.presentation.core.sample import Sample


class QtSample(Sample):
    def render(self):
        return QPushButton(self.content["name"])
