from ipywidgets import widgets

from pandas_profiling.report.presentation.core.sample import Sample


class WidgetSample(Sample):
    def render(self):
        return widgets.VBox([widgets.HTML(self.content["sample"])])
