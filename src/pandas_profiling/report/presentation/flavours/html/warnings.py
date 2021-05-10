from pandas_profiling.report.presentation.core.warnings import Warnings
from pandas_profiling.report.presentation.flavours.html import templates


class HTMLWarnings(Warnings):
    def render(self) -> str:
        styles = {
            "constant": "warning",
            "unsupported": "warning",
            "type_date": "warning",
            "constant_length": "primary",
            "high_cardinality": "primary",
            "unique": "primary",
            "uniform": "primary",
            "infinite": "info",
            "zeros": "info",
            "truncated": "info",
            "missing": "info",
            "skewed": "info",
            "high_correlation": "default",
            "duplicates": "default",
        }

        return templates.template("warnings.html").render(**self.content, styles=styles)
