from IPython.core.display import display
from ipywidgets import Output, widgets

from pandas_profiling.report.presentation.core.sample import Sample


class WidgetSample(Sample):
    def render(self):
        out = Output()
        with out:
            display(self.content["sample"])

        return widgets.VBox([out])
