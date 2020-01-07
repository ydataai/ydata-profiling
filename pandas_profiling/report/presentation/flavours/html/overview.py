from pandas_profiling.report.presentation.core.overview import Overview
from pandas_profiling.report.presentation.flavours.html import templates


class HTMLOverview(Overview):
    def render(self):
        return templates.template("info.html").render(**self.content)
