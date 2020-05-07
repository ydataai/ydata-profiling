from PyQt5.QtWidgets import QPushButton, QTabWidget, QVBoxLayout, QWidget

from pandas_profiling.report.presentation.abstract.renderable import Renderable
from pandas_profiling.report.presentation.core import Container


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


def get_list(items):
    list = QWidget()
    layout = QVBoxLayout()
    layout.addStretch(1)
    for item in items:
        layout.addWidget(item.render())
    list.setLayout(layout)
    return list


class QtContainer(Container):
    def render(self):
        # TODO: remove
        if self.sequence_type not in ["tabs", "variables", "sections", "accordion"]:
            self.sequence_type = "list"
        else:
            self.sequence_type = "tabs"

        if self.sequence_type == "tabs":
            return get_tabs(self.content["items"])
        elif self.sequence_type == "list":
            return get_list(self.content["items"])
        else:
            raise NotImplementedError()
