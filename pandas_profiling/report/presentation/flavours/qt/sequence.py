from PyQt5.QtWidgets import QTabWidget, QWidget
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QVBoxLayout

from pandas_profiling.report.presentation.abstract.renderable import Renderable
from pandas_profiling.report.presentation.core.sequence import Sequence


def get_name(item: Renderable):
    if hasattr(item, "name"):
        return item.name
    else:
        return item.anchor_id


def get_tabs(items):
    tabs = QTabWidget()

    # Tabs
    for item in items:
        tab1 = QWidget()
        tab1.layout = QVBoxLayout()
        tab1.layout.addWidget(item.render())
        tab1.setLayout(tab1.layout)

        tabs.addTab(tab1, get_name(item))

    return tabs


class QtSequence(Sequence):
    def render(self):
        # if self.sequence_type == "tabs":
        return get_tabs(self.content["items"])
        # raise NotImplementedError()
