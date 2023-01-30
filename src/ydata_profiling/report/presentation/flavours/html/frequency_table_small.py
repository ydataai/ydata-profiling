from ydata_profiling.report.presentation.core import FrequencyTableSmall
from ydata_profiling.report.presentation.flavours.html import templates


class HTMLFrequencyTableSmall(FrequencyTableSmall):
    def render(self) -> str:
        html = ""
        kwargs = self.content.copy()
        del kwargs["rows"]

        for idx, rows in enumerate(self.content["rows"]):
            html += templates.template("frequency_table_small.html").render(
                rows=rows, idx=idx, **kwargs
            )
        return html
