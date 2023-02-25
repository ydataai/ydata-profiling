from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, Optional

from pandas_profiling.model.description_target import TargetDescription


@dataclass
class BaseAnalysis:
    """Description of base analysis module of report.
    Overall info about report.

    Attributes
    ----------
    title : str
        Title of report.
    date_start : datetime
        Start of generating description.
    date_end : datetime
        End of generating description.
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
    """Description of DataFrame.

    Attributes
    ----------
    analysis : BaseAnalysis
        Base info about report.
        Title, start time and end time of description generating.
    table : Any
        DataFrame statistic. Base information about DataFrame.
    variables : Dict[str, Any]
        Description of variables (columns) of DataFrame.
        Key is column name, value is description dictionary.
    scatter : Any
        Pairwise scatter for all variables. Plot interactions between variables.
    correlations: Any
        Prepare correlation matrix for DataFrame
    missing: Any
        Describe missing values.
    alerts: Any
        Take alerts from all modules (variables, scatter, correlations), and group them.
    package: Any
        Contains version of pandas profiling and config.
    sample: Any
        Sample of data.
    duplicates: Any
        Description of duplicates.
    """

    analysis: BaseAnalysis
    table: Any
    target: Optional[TargetDescription]
    variables: Dict[str, Any]
    scatter: Any
    correlations: Any
    missing: Any
    alerts: Any
    package: Any
    sample: Any
    duplicates: Any
