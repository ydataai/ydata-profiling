from pandas_profiling.report.presentation.core.preview import Preview
from pandas_profiling.report.presentation.flavours.widget.sequence import WidgetSequence


class WidgetPreview(Preview):
    def render(self):
        if self.content["bottom"] is not None:
            items = [self.content["top"], self.content["bottom"]]
        else:
            items = [self.content["top"]]
        return WidgetSequence(items, sequence_type="variable").render()
