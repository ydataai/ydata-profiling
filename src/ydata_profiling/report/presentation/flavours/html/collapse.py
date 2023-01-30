from ydata_profiling.report.presentation.core import Collapse
from ydata_profiling.report.presentation.flavours.html import templates


class HTMLCollapse(Collapse):
    def render(self) -> str:
        return templates.template("collapse.html").render(**self.content)
