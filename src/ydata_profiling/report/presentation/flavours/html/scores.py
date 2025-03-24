"""
    Scores HTML renderer class
"""
from ydata_profiling.report.presentation.core.scores import Scores
from ydata_profiling.report.presentation.flavours.html import templates


# create the logic for this one
class HTMLScores(Scores):
    def render(self) -> str:
        return templates.template("scores.html").render(**self.content)
