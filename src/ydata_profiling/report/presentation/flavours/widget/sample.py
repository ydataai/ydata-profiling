from IPython.display import display
from ipywidgets import Output, widgets

from ydata_profiling.report.presentation.core.sample import Sample


class WidgetSample(Sample):
    def render(self) -> widgets.VBox:
        out = Output()
        with out:
            display(self.content["sample"])

        name = widgets.HTML(f"<h4>{self.content['name']}</h4>")
        return widgets.VBox([name, out])
