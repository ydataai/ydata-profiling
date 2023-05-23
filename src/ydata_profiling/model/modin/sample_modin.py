from typing import List

from ydata_profiling.config import Settings
from ydata_profiling.model.pandas.sample_pandas import pandas_get_sample
from ydata_profiling.model.sample import Sample, get_sample
from ydata_profiling.utils import modin


@get_sample.register(Settings, modin.DataFrame)
def modin_get_sample(config: Settings, df: modin.DataFrame) -> List[Sample]:
    return pandas_get_sample(config, df)
