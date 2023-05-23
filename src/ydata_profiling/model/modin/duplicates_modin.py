from typing import Any, Dict, Optional, Sequence, Tuple

from ydata_profiling.config import Settings
from ydata_profiling.model.duplicates import get_duplicates
from ydata_profiling.model.pandas.duplicates_pandas import pandas_get_duplicates
from ydata_profiling.utils import modin


@get_duplicates.register(Settings, modin.DataFrame, Sequence)
def modin_get_duplicates(
    config: Settings, df: modin.DataFrame, supported_columns: Sequence
) -> Tuple[Dict[str, Any], Optional[modin.DataFrame]]:
    return pandas_get_duplicates(config, df, supported_columns)
