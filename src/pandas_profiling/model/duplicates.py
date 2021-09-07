from typing import Optional, Sequence, Tuple, TypeVar

from multimethod import multimethod

from pandas_profiling.config import Settings
from pandas_profiling.model.schema import DuplicateResult

T = TypeVar("T")


@multimethod
def get_duplicates(
    config: Settings, df: T, supported_columns: Sequence
) -> Tuple[DuplicateResult, Optional[T]]:
    raise NotImplementedError()
