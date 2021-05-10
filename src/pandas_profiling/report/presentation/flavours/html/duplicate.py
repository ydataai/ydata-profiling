from pandas_profiling.report.presentation.core.duplicate import Duplicate
from pandas_profiling.report.presentation.flavours.html import templates


class HTMLDuplicate(Duplicate):
    def render(self) -> str:
        duplicate_html = self.content["duplicate"].to_html(
            classes="duplicate table table-striped"
        )
        return templates.template("duplicate.html").render(
            **self.content, duplicate_html=duplicate_html
        )
