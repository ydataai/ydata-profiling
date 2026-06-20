from typing import Any

from multimethod import multimethod

from data_profiling.config import Settings


@multimethod
def get_table_stats(config: Settings, df: Any, variable_stats: dict) -> dict:
    raise NotImplementedError()
