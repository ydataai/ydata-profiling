from typing import Any, Dict, Optional, Sequence, Tuple

from multimethod import multimethod

from pandas_profiling.config import Settings

T = TypeVar("T")

def get_duplicates(
    config: Settings, df: pd.DataFrame, supported_columns: Sequence
) -> Tuple[Dict[str, Any], Optional[pd.DataFrame]]:
    """Obtain the most occurring duplicate rows in the DataFrame.

    Args:
        config: report Settings object
        df: the Pandas DataFrame.
        supported_columns: the columns to consider

    Returns:
        A subset of the DataFrame, ordered by occurrence.
    """
    n_head = config.duplicates.head

    metrics: Dict[str, Any] = {}
    if n_head > 0:
        if supported_columns and len(df) > 0:
            duplicates_key = config.duplicates.key
            if duplicates_key in df.columns:
                raise ValueError(
                    f"Duplicates key ({duplicates_key}) may not be part of the DataFrame. Either change the "
                    f" column name in the DataFrame or change the 'duplicates.key' parameter."
                )

@multimethod
def get_duplicates(
    config: Settings, df: T, supported_columns: Sequence
) -> Tuple[Dict[str, Any], Optional[T]]:
    raise NotImplementedError()
