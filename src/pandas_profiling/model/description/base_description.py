from datetime import datetime
from typing import Any, Dict


class BaseAnalysis():
    def __init__(self, title: str, date_start:datetime, date_end:datetime) -> None:
        self.title = title
        self.date_start = date_start
        self.date_end = date_end

    @property
    def duration(self):
        return self.date_end - self.date_start

class BaseDescription():
    def __init__(
        self, 
        analysis:BaseAnalysis, 
        table, 
        variables, 
        scatter, 
        correlations, 
        missing, 
        alerts, 
        package, 
        sample, 
        duplicates
    ) -> None:
        self._analysis = analysis
        self._table = table
        self._variables = variables
        self._scatter = scatter
        self._correlations = correlations
        self._missing = missing
        self._alerts = alerts
        self._package = package
        self._sample = sample
        self._duplicates = duplicates
    
    @property
    def analysis(self) -> BaseAnalysis:
        return self._analysis
    
    @property
    def table(self):
        return self._table
    
    @property
    def variables(self):
        return self._variables

    @property
    def scatter(self):
        return self._scatter

    @property
    def correlations(self):
        return self._correlations

    @property
    def missing(self):
        return self._missing

    @property
    def alerts(self):
        return self._alerts

    @property
    def package(self):
        return self._package

    @property
    def sample(self):
        return self._sample

    @property
    def duplicates(self):
        return self._duplicates

    def to_dict(self) -> Dict[str, Any]:
        return {
            'analysis': self.analysis,
            'table': self.table,
            'variables': self.variables,
            'scatter': self.scatter,
            'correlations': self.correlations,
            'missing': self.missing,
            'alerts': self.alerts,
            'package': self.package,
            'sample': self.sample,
            'duplicates': self.duplicates,
        }