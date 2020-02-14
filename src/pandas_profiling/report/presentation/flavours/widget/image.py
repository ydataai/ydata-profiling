from ipywidgets import widgets

from pandas_profiling.report.presentation.core.image import Image


class WidgetImage(Image):
    def render(self):
        image = self.content["image"]
        if self.content["image_format"] == "svg":
            image.replace("svg ", 'svg class="img-responsive center-img"')
        else:
            image = '<img src="{image}" alt="{alt}" />'.format(
                image=image, alt=self.content["alt"]
            )

        widget = widgets.HTML(image)
        if "caption" in self.content and self.content["caption"] is not None:
            caption = widgets.HTML(
                '<p style="color: #999"><em>{caption}</em></p>'.format(
                    caption=self.content["caption"]
                )
            )
            return widgets.VBox([widget, caption])
        else:
            return widget
