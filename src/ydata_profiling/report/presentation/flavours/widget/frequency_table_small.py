from typing import List

from ipywidgets import widgets

from ydata_profiling.report.presentation.core.frequency_table_small import (
    FrequencyTableSmall,
)


class WidgetFrequencyTableSmall(FrequencyTableSmall):
    def render(self) -> widgets.VBox:
        return frequency_table_nb(self.content["rows"])


def frequency_table_nb(rows: List[List[dict]]) -> widgets.VBox:
    items = []

    fq_rows = rows[0]
    for row in fq_rows:
        if row["extra_class"] == "missing":
            items.append(
                widgets.HBox(
                    [
                        widgets.FloatProgress(
                            value=row["count"],
                            min=0,
                            max=row["n"],
                            description=str(row["label"]),
                            bar_style="danger",
                        ),
                        widgets.Label(str(row["count"])),
                    ]
                )
            )
        elif row["extra_class"] == "other":
            items.append(
                widgets.HBox(
                    [
                        widgets.FloatProgress(
                            value=row["count"],
                            min=0,
                            max=row["n"],
                            description=str(row["label"]),
                            bar_style="info",
                        ),
                        widgets.Label(str(row["count"])),
                    ]
                )
            )
        else:
            items.append(
                widgets.HBox(
                    [
                        widgets.FloatProgress(
                            value=row["count"],
                            min=0,
                            max=row["n"],
                            description=str(row["label"]),
                            bar_style="",
                        ),
                        widgets.Label(str(row["count"])),
                    ]
                )
            )

    return widgets.VBox(items)
