from pandas_profiling.report.presentation.core.correlation_table import CorrelationTable
from pandas_profiling.report.presentation.flavours.html import templates


class HTMLCorrelationTable(CorrelationTable):
    def render(self) -> str:
        correlation_matrix_html = self.content["correlation_matrix"].to_html(
            classes="correlation-table table table-striped",
            float_format="{:.3f}".format,
        )
        return templates.template("correlation_table.html").render(
            **self.content, correlation_matrix_html=correlation_matrix_html
        )
