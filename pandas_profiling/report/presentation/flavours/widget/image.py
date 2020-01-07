from ipywidgets import widgets

from pandas_profiling.report.presentation.core.image import Image


class WidgetImage(Image):
    def render(self):
        widget = widgets.HTML(
            "<img src=\"{image}\" alt=\"{alt}\" />".format(image=self.content['image'], alt=self.content['alt'])
        )
        if "caption" in self.content and self.content["caption"] is not None:
            caption = widgets.HTML(
                '<p style="color: #999"><em>{caption}</em></p>'.format(caption=self.content["caption"])
            )
            return widgets.VBox([widget, caption])
        else:
            return widget
