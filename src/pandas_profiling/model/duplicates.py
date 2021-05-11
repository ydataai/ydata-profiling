from typing import Any, Dict, Optional, Sequence, Tuple, TypeVar

from multimethod import multimethod

from pandas_profiling.config import Settings

T = TypeVar("T")


@multimethod
def get_duplicates(
    config: Settings, df: T, supported_columns: Sequence
) -> Tuple[Dict[str, Any], Optional[T]]:
    raise NotImplementedError()
