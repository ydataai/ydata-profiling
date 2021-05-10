from pandas_profiling.report.presentation.core import FrequencyTableSmall
from pandas_profiling.report.presentation.flavours.html import templates


class HTMLFrequencyTableSmall(FrequencyTableSmall):
    def render(self) -> str:
        return templates.template("frequency_table_small.html").render(**self.content)
