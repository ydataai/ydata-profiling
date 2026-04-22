from ydata_profiling.report.presentation.core import Table
from ydata_profiling.report.presentation.flavours.html import templates


class HTMLTable(Table):
    def render(self) -> str:
        return templates.template("table.html").render(**self.content)
