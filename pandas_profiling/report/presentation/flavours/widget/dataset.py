from ipywidgets import widgets

from pandas_profiling.report.presentation.core import Dataset
from pandas_profiling.report.presentation.flavours.html import templates


class WidgetDataset(Dataset):
    def render(self):
        return widgets.HTML(
            templates.template("overview/overview.html").render(**self.content)
        )
