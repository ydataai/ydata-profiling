from typing import Any, Dict, Optional, Sequence, Tuple

import pyspark.sql.functions as F
from pyspark.sql import DataFrame

from ydata_profiling.config import Settings
from ydata_profiling.model.duplicates import get_duplicates


@get_duplicates.register
def get_duplicates_spark(
    config: Settings, df: DataFrame, supported_columns: Sequence
) -> Tuple[Dict[str, Any], Optional[DataFrame]]:
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
    if n_head == 0:
        return metrics, None

    if not supported_columns or df.count() == 0:
        metrics["n_duplicates"] = 0
        metrics["p_duplicates"] = 0.0
        return metrics, None

    duplicates_key = config.duplicates.key
    if duplicates_key in df.columns:
        raise ValueError(
            f"Duplicates key ({duplicates_key}) may not be part of the DataFrame. Either change the "
            f" column name in the DataFrame or change the 'duplicates.key' parameter."
        )

    duplicated_df = (
        df.groupBy(df.columns)
        .agg(F.count("*").alias(duplicates_key))
        .withColumn(duplicates_key, F.col(duplicates_key).cast("int"))
        .filter(F.col(duplicates_key) > 1)
    )

    metrics["n_duplicates"] = duplicated_df.count()
    metrics["p_duplicates"] = metrics["n_duplicates"] / df.count()

    return metrics, (
        duplicated_df.orderBy(duplicates_key, ascending=False).limit(n_head).toPandas()
    )
