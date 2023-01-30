from ydata_profiling.report.presentation.core.table import Table
from ydata_profiling.report.presentation.flavours.html import templates


class HTMLTable(Table):
    def render(self) -> str:
        return templates.template("table.html").render(**self.content)
