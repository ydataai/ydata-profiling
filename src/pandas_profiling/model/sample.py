from functools import singledispatch
from typing import List

import attr

from pandas_profiling.model.dataframe_wrappers import (
    GenericDataFrame,
    PandasDataFrame,
    SparkDataFrame,
)


@attr.s
class Sample:
    id = attr.ib()
    data = attr.ib()
    name = attr.ib()
    caption = attr.ib(default=None)


@singledispatch
def get_sample(df: GenericDataFrame) -> List[Sample]:
    raise NotImplementedError("This method is not implemented.")


from pandas_profiling.model.sample_pandas import get_sample_pandas
from pandas_profiling.model.sample_spark import get_sample_spark

get_sample.register(PandasDataFrame, get_sample_pandas)
get_sample.register(SparkDataFrame, get_sample_spark)
