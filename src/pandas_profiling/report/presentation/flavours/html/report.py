from pandas_profiling.report.presentation.core.report import Report
from pandas_profiling.report.presentation.flavours.html import templates


class HTMLReport(Report):
    def render(self, **kwargs):
        nav_items = [
            (section.name, section.anchor_id)
            for section in self.content["body"].content["items"]
        ]

        return templates.template("report.html").render(
            **self.content, nav_items=nav_items, **kwargs
        )
