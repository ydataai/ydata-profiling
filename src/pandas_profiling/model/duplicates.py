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
        return (
            df[df.duplicated(subset=supported_columns, keep=False)]
            .groupby(supported_columns)
            .size()
            .reset_index(name="count")
            .nlargest(n_head, "count")
        )
    return None
