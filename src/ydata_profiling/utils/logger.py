"""
    Logger function for ydata-profiling reports
"""
from __future__ import absolute_import, division, print_function

import logging

import pandas as pd

from ydata_profiling.utils.common import analytics_features

class ProfilingLogger(logging.Logger):
    def __init__(self, name, level=logging.INFO):
        super().__init__(name, level)

    def info(
            self,
            msg: object,
        ) -> None:
        super().info(f'[PROFILING] - {msg}.')

    def info_def_report(self, dataframe, timeseries: bool):
        if dataframe == pd.DataFrame:
            dataframe = 'pandas'
            report_type = 'regular'
        elif dataframe == type(None):
            dataframe = 'pandas'
            report_type='compare'
        else:
            dataframe = 'spark'
            report_type = 'regular'

        datatype='timeseries' if timeseries else 'tabular'

        analytics_features(dataframe=dataframe,
                           datatype=datatype,
                           report_type=report_type)

        super().info(f'[PROFILING] Calculating profile with the following characteristics '
                     f'- {dataframe} | {datatype} | {report_type}.')