from typing import Any

from multimethod import multimethod

from pandas_profiling.config import Settings
from pandas_profiling.model.schema import TableResult


@multimethod
def get_table_stats(config: Settings, df: Any, variable_stats: dict) -> TableResult:
    raise NotImplementedError()
