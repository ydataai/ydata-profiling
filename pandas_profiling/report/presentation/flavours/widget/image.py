from ipywidgets import widgets

from pandas_profiling.report.presentation.core.image import Image


class WidgetImage(Image):
    def render(self):
        widget = widgets.HTML(
            f"<img src=\"{self.content['image']}\" alt=\"{self.content['alt']}\" />"
        )
        if "caption" in self.content and self.content["caption"] is not None:
            caption = widgets.HTML(
                f'<p style="color: #999"><em>{self.content["caption"]}</em></p>'
            )
            return widgets.VBox([widget, caption])
        else:
            return widget
