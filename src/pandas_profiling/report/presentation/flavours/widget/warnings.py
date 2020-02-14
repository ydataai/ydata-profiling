from ipywidgets import widgets

from pandas_profiling.report.presentation.core import Warnings
from pandas_profiling.report.presentation.flavours.html import templates


class WidgetWarnings(Warnings):
    def render(self):
        return widgets.HTML(templates.template("warnings.html").render(**self.content))
