from IPython.display import display
from ipywidgets import Output, widgets

from ydata_profiling.report.presentation.core.correlation_table import CorrelationTable


class WidgetCorrelationTable(CorrelationTable):
    def render(self) -> widgets.VBox:
        out = Output()
        with out:
            display(self.content["correlation_matrix"])

        name = widgets.HTML(f"<h4>{self.content['name']}</h4>")
        return widgets.VBox([name, out])
