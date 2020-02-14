from pandas_profiling.report.presentation.core import HTML


class HTMLHTML(HTML):
    def render(self):
        return self.content["html"]
