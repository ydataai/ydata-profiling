from pandas_profiling.report.presentation.core import LogOddsTable
from pandas_profiling.report.presentation.flavours.html import templates


class HTMLLogOddsTable(LogOddsTable):
    def render(self) -> str:
        return templates.template("log_odds_table.html").render(**self.content, idx=2)
