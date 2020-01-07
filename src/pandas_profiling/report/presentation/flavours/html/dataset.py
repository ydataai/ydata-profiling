from pandas_profiling.report.presentation.core import Dataset
from pandas_profiling.report.presentation.flavours.html import templates


class HTMLDataset(Dataset):
    def render(self):
        return templates.template("overview/overview.html").render(**self.content)
