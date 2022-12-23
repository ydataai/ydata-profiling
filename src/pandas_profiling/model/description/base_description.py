from datetime import datetime


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
        self.analysis = analysis
        self.table = table
        self.variables = variables
        self.scatter = scatter
        self.correlations = correlations
        self.missing = missing
        self.alerts = alerts
        self.package = package
        self.sample = sample
        self.duplicates = duplicates