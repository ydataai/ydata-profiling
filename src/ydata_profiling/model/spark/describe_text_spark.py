from typing import Tuple

from pyspark.sql import DataFrame

from ydata_profiling.config import Settings


def describe_text_1d_spark(
    config: Settings, df: DataFrame, summary: dict
) -> Tuple[Settings, DataFrame, dict]:
    """Describe a categorical series.

    Args:
        series: The Series to describe.
        summary: The dict containing the series description so far.

    Returns:
        A dict containing calculated series description values.
    """

    redact = config.vars.text.redact
    if not redact:
        summary["first_rows"] = df.limit(5).toPandas().squeeze("columns")

    return config, df, summary
