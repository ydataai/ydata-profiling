from ydata_profiling.report.presentation.core import FrequencyTable
from ydata_profiling.report.presentation.flavours.html import templates


class HTMLFrequencyTable(FrequencyTable):
    def render(self) -> str:
        if isinstance(self.content["rows"][0], list):
            html = ""

            kwargs = self.content.copy()
            del kwargs["rows"]
            for idx, rows in enumerate(self.content["rows"]):
                html += templates.template("frequency_table.html").render(
                    rows=rows, idx=idx, **kwargs
                )
            return html
        else:
            return templates.template("frequency_table.html").render(
                **self.content, idx=0
            )
