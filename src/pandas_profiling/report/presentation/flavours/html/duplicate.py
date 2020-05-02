from pandas_profiling.report.presentation.core.duplicate import Duplicate
from pandas_profiling.report.presentation.flavours.html import templates


class HTMLDuplicate(Duplicate):
    def render(self):
        return templates.template("duplicate.html").render(**self.content)
