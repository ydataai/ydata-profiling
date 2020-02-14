from pandas_profiling.report.presentation.core import Variable
from pandas_profiling.report.presentation.flavours.qt.sequence import QtSequence


class QtVariable(Variable):
    def render(self):
        if self.content["bottom"] is not None:
            items = [self.content["top"], self.content["bottom"]]
        else:
            items = [self.content["top"]]
        return QtSequence(items, sequence_type="list").render()
