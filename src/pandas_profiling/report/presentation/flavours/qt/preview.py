from pandas_profiling.report.presentation.core.preview import Preview
from pandas_profiling.report.presentation.flavours.qt.sequence import QtSequence


class QtPreview(Preview):
    def render(self):
        if self.content["bottom"] is not None:
            items = [self.content["top"], self.content["bottom"]]
        else:
            items = [self.content["top"]]
        return QtSequence(items, sequence_type="list").render()
