from pandas_profiling.report.presentation.core.input import InputBox
from pandas_profiling.report.presentation.flavours.html import templates


class HTMLInputBox(InputBox):
    def render(self) -> str:
        return templates.template("input.html").render(**self.content)
