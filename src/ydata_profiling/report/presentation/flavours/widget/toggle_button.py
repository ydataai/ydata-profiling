from ipywidgets import widgets

from ydata_profiling.report.presentation.core import ToggleButton


class WidgetToggleButton(ToggleButton):
    def render(self) -> widgets.HBox:
        toggle = widgets.ToggleButton(description=self.content["text"])
        toggle.layout.width = "fit-content"

        toggle_box = widgets.HBox([toggle])
        toggle_box.layout.align_items = "flex-end"
        toggle_box.layout.display = "flex"
        toggle_box.layout.flex_flow = "column"
        toggle_box.layout.width = "100%"

        return toggle_box
