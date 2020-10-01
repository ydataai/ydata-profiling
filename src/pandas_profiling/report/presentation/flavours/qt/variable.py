from pandas_profiling.report.presentation.core import Variable
from pandas_profiling.report.presentation.flavours.qt.container import QtContainer


class QtVariable(Variable):
    def render(self):
        if self.content["bottom"] is not None:
            items = [self.content["top"], self.content["bottom"]]
        else:
            items = [self.content["top"]]
        return QtContainer(items, sequence_type="list").render()
