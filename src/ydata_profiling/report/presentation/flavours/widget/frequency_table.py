from typing import List, Tuple

from ipywidgets import GridspecLayout, VBox, widgets

from ydata_profiling.report.presentation.core.frequency_table import FrequencyTable


def get_table(
    items: List[Tuple[widgets.Label, widgets.FloatProgress, widgets.Label]]
) -> VBox:
    table = GridspecLayout(len(items), 3)
    for row_id, (label, progress, count) in enumerate(items):
        table[row_id, 0] = label
        table[row_id, 1] = progress
        table[row_id, 2] = count

    return VBox([table])


class WidgetFrequencyTable(FrequencyTable):
    def render(self) -> VBox:
        items = []

        rows = self.content["rows"][0]
        for row in rows:
            if row["extra_class"] == "missing":
                items.append(
                    (
                        widgets.Label(str(row["label"])),
                        widgets.FloatProgress(
                            value=row["count"], min=0, max=row["n"], bar_style="danger"
                        ),
                        widgets.Label(str(row["count"])),
                    )
                )
            elif row["extra_class"] == "other":
                items.append(
                    (
                        widgets.Label(str(row["label"])),
                        widgets.FloatProgress(
                            value=row["count"], min=0, max=row["n"], bar_style="info"
                        ),
                        widgets.Label(str(row["count"])),
                    )
                )
            else:
                items.append(
                    (
                        widgets.Label(str(row["label"])),
                        widgets.FloatProgress(
                            value=row["count"], min=0, max=row["n"], bar_style=""
                        ),
                        widgets.Label(str(row["count"])),
                    )
                )

        return get_table(items)
