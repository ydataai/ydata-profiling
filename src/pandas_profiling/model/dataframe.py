from typing import Any

from multimethod import multimethod
from pandas_profiling.config import Settings


@multimethod
def check_dataframe(config: Settings, df: Any) -> None:
    raise NotImplementedError()


@multimethod
def preprocess(df: Any) -> Any:
    return df
