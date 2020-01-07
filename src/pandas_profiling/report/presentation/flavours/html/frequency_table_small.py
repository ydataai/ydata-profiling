from pandas_profiling.report.presentation.core.frequency_table_small import (
    FrequencyTableSmall,
)
from pandas_profiling.report.presentation.flavours.html import templates


class HTMLFrequencyTableSmall(FrequencyTableSmall):
    def render(self):
        return templates.template("frequency_table_small.html").render(
            rows=self.content
        )
