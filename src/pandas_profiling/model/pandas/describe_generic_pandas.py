from typing import Tuple

import pandas as pd

from pandas_profiling.config import Settings
from pandas_profiling.model.summary_algorithms import describe_generic


@describe_generic.register
def pandas_describe_generic(
    config: Settings, series: pd.Series, summary: dict
) -> Tuple[Settings, pd.Series, dict]:
    """Describe generic series.

    Args:
        config: report Settings object
        series: The Series to describe.
        summary: The dict containing the series description so far.

    Returns:
        A dict containing calculated series description values.
    """

    # number of observations in the Series
    length = len(series)

    summary.update(
        {
            "n": length,
            "p_missing": summary["n_missing"] / length if length > 0 else 0,
            "count": length - summary["n_missing"],
            "memory_size": series.memory_usage(deep=config.memory_deep),
        }
    )

    return config, series, summary
