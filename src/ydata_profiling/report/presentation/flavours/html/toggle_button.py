from ydata_profiling.report.presentation.core import ToggleButton
from ydata_profiling.report.presentation.flavours.html import templates


class HTMLToggleButton(ToggleButton):
    def render(self) -> str:
        return templates.template("toggle_button.html").render(**self.content)
