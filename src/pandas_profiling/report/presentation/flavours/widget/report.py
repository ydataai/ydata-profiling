from ipywidgets import widgets

from pandas_profiling.report.presentation.core.report import Report


class WidgetReport(Report):
    def render(self):
        return widgets.VBox([self.content["body"], self.content["footer"]])
