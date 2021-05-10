from pandas_profiling.report.presentation.core import FrequencyTable
from pandas_profiling.report.presentation.flavours.html import templates


class HTMLFrequencyTable(FrequencyTable):
    def render(self) -> str:
        return templates.template("frequency_table.html").render(**self.content)
