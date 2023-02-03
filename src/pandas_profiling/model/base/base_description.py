from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict


@dataclass
class BaseAnalysis:
    """Description of base analysis module of report.
    Overall info about report.
    """

    title: str
    date_start: datetime
    date_end: datetime

    def __init__(self, title: str, date_start: datetime, date_end: datetime) -> None:
        self.title = title
        self.date_start = date_start
        self.date_end = date_end

    @property
    def duration(self):
        return self.date_end - self.date_start


@dataclass
class BaseDescription:
    analysis: BaseAnalysis
    table: Any
    variables: Any
    scatter: Any
    correlations: Any
    missing: Any
    alerts: Any
    package: Any
    sample: Any
    duplicates: Any
