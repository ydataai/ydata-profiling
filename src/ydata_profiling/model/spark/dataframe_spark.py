import warnings

from pyspark.sql import DataFrame
from pyspark.sql.types import MapType

from ydata_profiling.config import Settings


def spark_preprocess(config: Settings, df: DataFrame) -> DataFrame:
    """Preprocess the Spark DataFrame by removing MapType columns.
    - Excludes columns of type MapType
    - Raises a warning if any MapType columns are removed

    Args:
        config: Report settings object
        df: The Spark DataFrame

    Returns:
        The preprocessed DataFrame without MapType columns.
    """
    # Identify MapType columns
    columns_to_remove = [
        field.name for field in df.schema.fields if isinstance(field.dataType, MapType)
    ]

    if columns_to_remove:
        warnings.warn(
            f"""Spark DataFrame profiling does not handle MapTypes. Column(s) {', '.join(columns_to_remove)} will be ignored.
            To fix this, consider converting your MapType into a StructType or extracting key-value pairs using `explode()`.
            """
        )
        df = df.drop(*columns_to_remove)

    return df  # Return unchanged DataFrame if no MapType columns exist
