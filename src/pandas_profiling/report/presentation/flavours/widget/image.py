from ipywidgets import widgets

from pandas_profiling.report.presentation.core.image import Image


class WidgetImage(Image):
    def render(self):
        image = self.content["image"]
        if self.content["image_format"] == "svg":
            image.replace("svg ", 'svg class="img-responsive center-img"')
        else:
            alt = self.content["alt"]
            image = f'<img src="{image}" alt="{alt}" />'

        widget = widgets.HTML(image)
        if "caption" in self.content and self.content["caption"] is not None:
            caption = self.content["caption"]
            caption = widgets.HTML(f'<p style="color: #999"><em>{caption}</em></p>')
            return widgets.VBox([widget, caption])
        else:
            return widget
