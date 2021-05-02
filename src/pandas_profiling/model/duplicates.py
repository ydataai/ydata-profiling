from functools import singledispatch
from typing import Any, Dict, Optional, Tuple

import pandas as pd

from pandas_profiling.model.dataframe_wrappers import (
    GenericDataFrame,
    PandasDataFrame,
    SparkDataFrame,
)
from pandas_profiling.model.duplicates_pandas import get_duplicates_pandas
from pandas_profiling.model.duplicates_spark import get_duplicates_spark


@singledispatch
def get_duplicates(
    df: GenericDataFrame, supported_columns
) -> Tuple[Dict[str, Any], Optional[pd.DataFrame]]:
    raise NotImplementedError("This method is not implemented.")


get_duplicates.register(PandasDataFrame, get_duplicates_pandas)
get_duplicates.register(SparkDataFrame, get_duplicates_spark)
