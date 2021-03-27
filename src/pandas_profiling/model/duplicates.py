from typing import Optional

import pandas as pd

from pandas_profiling.config import config


def get_duplicates(df: pd.DataFrame, supported_columns) -> Optional[pd.DataFrame]:
    """Obtain the most occurring duplicate rows in the DataFrame.

    Args:
        df: the Pandas DataFrame.
        supported_columns: the columns to consider

    Returns:
        A subset of the DataFrame, ordered by occurrence.
    """
    n_head = config["duplicates"]["head"].get(int)

    if n_head > 0 and supported_columns:
        duplicates_key = config["duplicates"]["key"].get(str)
        if duplicates_key in df.columns:
            raise ValueError(
                f"Duplicates key ({duplicates_key}) may not be part of the DataFrame. Either change the "
                f" column name in the DataFrame or change the 'duplicates.key' parameter."
            )

        return (
            df[df.duplicated(subset=supported_columns, keep=False)]
            .groupby(supported_columns)
            .size()
            .reset_index(name=duplicates_key)
            .nlargest(n_head, duplicates_key)
        )
    return None
