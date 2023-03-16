from typing import List, Tuple

from ipywidgets import GridspecLayout, VBox, widgets
from pandas_profiling.report.presentation.core import LogOddsTable


def get_table(
    items: List[Tuple[widgets.Label, widgets.FloatProgress, widgets.Label]]
) -> VBox:
    table = GridspecLayout(len(items), 4)
    for row_id, (label, progress, positive_count, negative_count) in enumerate(items):
        table[row_id, 0] = label
        table[row_id, 1] = progress
        table[row_id, 2] = positive_count
        table[row_id, 2] = negative_count

    return VBox([table])


# TODO create widgets for log odds table
class WidgetLogOddsTable(LogOddsTable):
    def render(self) -> VBox:
        items = []

        rows = self.content["rows"][0]
        for row in rows:
            items.append(
                (
                    widgets.Label(str(row["label"])),
                    widgets.FloatProgress(
                        value=row["log_odds_ratio"], min=0, max=row["max"], bar_style=""
                    ),
                    widgets.Label(str(row["positive_count"])),
                    widgets.Label(str(row["negative_count"])),
                )
            )

        return get_table(items)
