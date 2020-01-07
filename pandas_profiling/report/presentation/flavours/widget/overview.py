from ipywidgets import widgets

from pandas_profiling.report.presentation.core.overview import Overview
from pandas_profiling.report.presentation.flavours.html import templates


class WidgetOverview(Overview):
    def render(self):
        return widgets.HTML(templates.template("info.html").render(**self.content))
