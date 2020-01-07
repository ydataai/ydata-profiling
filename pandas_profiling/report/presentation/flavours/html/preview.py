from pandas_profiling.report.presentation.core.preview import Preview
from pandas_profiling.report.presentation.flavours.html import templates


class HTMLPreview(Preview):
    def render(self):
        return templates.template("preview.html").render(**self.content)
