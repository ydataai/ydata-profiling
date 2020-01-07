from IPython.core.display import display
from ipywidgets import widgets, HTML

from pandas_profiling.report.presentation.core.frequency_table import FrequencyTable


class WidgetFrequencyTable(FrequencyTable):
    def render(self):
        items = []

        for row in self.content["rows"]:
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

        ft = widgets.VBox(items)

        # Overwrite info to disabled
        # TODO: resize width of progress bar / label
        # display(
        #     HTML(
        #         "<style>.progress-bar-info{background-color: #ddd !important;} .dataframe td{     white-space: nowrap !important;}</style>"
        #     )
        # )
        return ft
