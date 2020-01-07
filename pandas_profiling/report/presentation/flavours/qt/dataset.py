from PyQt5.QtWidgets import QPushButton

from pandas_profiling.report.presentation.core import Dataset


class QtDataset(Dataset):
    def render(self):
        return QPushButton("PyQt5 button")
