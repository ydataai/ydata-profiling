from pandas_profiling.report.presentation.core import Image
from pandas_profiling.report.presentation.flavours.html import templates


class HTMLImage(Image):
    def render(self) -> str:
        return templates.template("diagram.html").render(**self.content)
