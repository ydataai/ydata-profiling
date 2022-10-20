from ipywidgets import widgets

from pandas_profiling.report.presentation.core import Dropdown


class WidgetDropdown(Dropdown):
    def render(self) -> widgets.VBox:
        dropdown = widgets.Dropdown(
            options=self.content["items"], description=self.content["name"]
        )
        titles = []
        item = self.content["item"].content["items"]
        for i in item:
            titles.append(i.name)
        item = self.content["item"].render()

        def change_view(widg: dict) -> None:
            if dropdown.value == "":
                item.selected_index = None
            else:
                for i in range(len(titles)):
                    if titles[i] == dropdown.value:
                        item.selected_index = i
                        break

        dropdown.observe(change_view, names=["value"])

        if self.content["item"] is not None:
            return widgets.VBox([dropdown, item])
        else:
            return widgets.Vbox([dropdown])
