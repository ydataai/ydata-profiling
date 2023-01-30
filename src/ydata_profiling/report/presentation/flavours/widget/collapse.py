from ipywidgets import Box, widgets

from ydata_profiling.report.presentation.core import Collapse


class WidgetCollapse(Collapse):
    def render(self) -> widgets.VBox:
        if self.content["button"].anchor_id == "toggle-correlation-description":
            collapse = "correlation"
        else:
            collapse = "variable"

        toggle = self.content["button"].render()
        item = self.content["item"].render()

        if collapse == "correlation":

            def toggle_func(widg: dict) -> None:
                if widg["new"]:
                    display = ""
                    grid = "50% 50%"
                else:
                    display = "none"
                    grid = ""

                for c in item.children:
                    if isinstance(c, Box):
                        c.children[1].layout.display = display
                    c.layout.grid_template_columns = grid

        else:

            def toggle_func(widg: dict) -> None:
                if widg["new"]:
                    display = ""
                else:
                    display = "none"
                item.layout.display = display

        toggle_func({"new": False})
        toggle.children[0].observe(toggle_func, names=["value"])

        return widgets.VBox([toggle, item])
