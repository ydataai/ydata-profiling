"""
    Logger function for ydata-profiling reports
"""

import logging

import pandas as pd

from ydata_profiling.utils.common import (
    analytics_features,
    calculate_nrows,
    is_running_in_databricks,
)


class ProfilingLogger(logging.Logger):
    def __init__(self, name: str, level: int = logging.INFO):
        super().__init__(name, level)

    def info_def_report(self, df, timeseries: bool) -> None:  # noqa: ANN001
        try:
            ncols = len(df.columns)
        except AttributeError:
            ncols = 0

        nrows = calculate_nrows(df)

        if isinstance(df, pd.DataFrame):
            dataframe = "pandas"
            report_type = "regular"
        elif df is None:
            dataframe = "pandas"
            report_type = "compare"
        else:
            dataframe = "spark"
            report_type = "regular"

        dbx = is_running_in_databricks()
        datatype = "timeseries" if timeseries else "tabular"

        analytics_features(
            dataframe=dataframe,
            datatype=datatype,
            report_type=report_type,
            nrows=nrows,
            ncols=ncols,
            dbx=dbx,
        )

        super().info(
            f"[PROFILING] Calculating profile with the following characteristics "
            f"- {dataframe} | {datatype} | {report_type}."
        )
