from PyQt5.QtWidgets import QPushButton

from pandas_profiling.report.presentation.core.root import Root


class QtRoot(Root):
    def render(self, **kwargs):
        return QPushButton("Root")
