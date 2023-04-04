from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any, Dict, List, Union


@dataclass
class BaseAnalysis:
    """Description of base analysis module of report.
    Overall info about report.

    Attributes
        title (str): Title of report.
        date_start (Union[datetime, List[datetime]]): Start of generating description.
        date_end (Union[datetime, List[datetime]]): End of generating description.
    """

    title: str
    date_start: Union[datetime, List[datetime]]
    date_end: Union[datetime, List[datetime]]

    def __init__(self, title: str, date_start: datetime, date_end: datetime) -> None:
        self.title = title
        self.date_start = date_start
        self.date_end = date_end

    @property
    def duration(self) -> Union[timedelta, List[timedelta]]:
        if isinstance(self.date_start, datetime) and isinstance(
            self.date_end, datetime
        ):
            return self.date_end - self.date_start
        if isinstance(self.date_start, list) and isinstance(self.date_end, list):
            return [
                self.date_end[i] - self.date_start[i]
                for i in range(len(self.date_start))
            ]
        else:
            raise ValueError()


@dataclass
class BaseDescription:
    """Description of DataFrame.

    Attributes:
        analysis (BaseAnalysis): Base info about report. Title, start time and end time of description generating.
        table (Any): DataFrame statistic. Base information about DataFrame.
        variables (Dict[str, Any]): Description of variables (columns) of DataFrame. Key is column name, value is description dictionary.
        scatter (Any): Pairwise scatter for all variables. Plot interactions between variables.
        correlations (Dict[str, Any]): Prepare correlation matrix for DataFrame
        missing (Dict[str, Any]): Describe missing values.
        alerts (Any): Take alerts from all modules (variables, scatter, correlations), and group them.
        package (Dict[str, Any]): Contains version of pandas profiling and config.
        sample (Any): Sample of data.
        duplicates (Any): Description of duplicates.
    """

    analysis: BaseAnalysis
    table: Any
    variables: Dict[str, Any]
    scatter: Any
    correlations: Dict[str, Any]
    missing: Dict[str, Any]
    alerts: Any
    package: Dict[str, Any]
    sample: Any
    duplicates: Any
