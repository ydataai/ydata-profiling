from typing import Any, Dict, Optional, Tuple

import pandas as pd

from pandas_profiling.config import Settings


def get_duplicates(
    config: Settings, df: pd.DataFrame, supported_columns
) -> Tuple[Dict[str, Any], Optional[pd.DataFrame]]:
    """Obtain the most occurring duplicate rows in the DataFrame.

    Args:
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

            duplicated_rows = df.duplicated(subset=supported_columns, keep=False)
            duplicated_rows = (
                df[duplicated_rows]
                .groupby(supported_columns)
                .size()
                .reset_index(name=duplicates_key)
            )

            metrics["n_duplicates"] = len(duplicated_rows[duplicates_key])
            metrics["p_duplicates"] = metrics["n_duplicates"] / len(df)

            return (
                metrics,
                duplicated_rows.nlargest(n_head, duplicates_key),
            )
        else:
            metrics["n_duplicates"] = 0
            metrics["p_duplicates"] = 0.0
            return metrics, None
    else:
        return metrics, None
