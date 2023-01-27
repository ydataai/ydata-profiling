import pandas as pd

from ydata_profiling.report.presentation.core.duplicate import Duplicate
from ydata_profiling.report.presentation.flavours.html import templates


def to_html(df: pd.DataFrame) -> str:
    html = df.to_html(
        classes="duplicate table table-striped",
    )
    if df.empty:
        html = html.replace(
            "<tbody>",
            f"<tbody><tr><td colspan={len(df.columns) + 1}>Dataset does not contain duplicate rows.</td></tr>",
        )
    return html


class HTMLDuplicate(Duplicate):
    def render(self) -> str:
        duplicate_html = to_html(self.content["duplicate"])
        return templates.template("duplicate.html").render(
            **self.content, duplicate_html=duplicate_html
        )
