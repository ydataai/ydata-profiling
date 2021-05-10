from ipywidgets import widgets

from pandas_profiling.report.presentation.core import VariableInfo
from pandas_profiling.report.presentation.flavours.html import templates


class WidgetVariableInfo(VariableInfo):
    def render(self) -> widgets.HTML:
        return widgets.HTML(
            templates.template("variable_info.html").render(**self.content)
        )
