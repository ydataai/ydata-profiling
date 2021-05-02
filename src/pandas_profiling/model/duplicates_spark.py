from typing import Any, Dict, List, Optional, Tuple

import pandas as pd

from pandas_profiling.config import config
from pandas_profiling.model.dataframe_wrappers import SparkDataFrame


def get_duplicates_spark(
    df: SparkDataFrame, supported_columns: List[str]
) -> Tuple[Dict[str, Any], Optional[pd.DataFrame]]:
    """Obtain the most occurring duplicate rows in the DataFrame.

    Args:
        df: the Pandas DataFrame.
        supported_columns: the columns to consider
        n_head: top n duplicate values to return

    Returns:
        A subset of the DataFrame, ordered by occurrence.
    """
    n_head = config["duplicates"]["head"].get(int)

    return df.groupby_get_n_largest_dups(supported_columns, n_head)
