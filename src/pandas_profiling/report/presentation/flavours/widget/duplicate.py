from ipywidgets import widgets

from pandas_profiling.report.presentation.core.duplicate import Duplicate


class WidgetDuplicate(Duplicate):
    def render(self):
        return widgets.VBox([widgets.HTML(self.content["duplicate"])])
