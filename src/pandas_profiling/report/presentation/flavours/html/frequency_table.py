from pandas_profiling.report.presentation.flavours.html import templates
from pandas_profiling.report.presentation.core import FrequencyTable


class HTMLFrequencyTable(FrequencyTable):
    def render(self):
        return templates.template("frequency_table.html").render(
            rows=self.content["rows"]
        )
