from PyQt5.QtWidgets import QPushButton

from pandas_profiling.report.presentation.core.preview import Preview


class QtPreview(Preview):
    def render(self):
        return QPushButton("PyQt5 button")
