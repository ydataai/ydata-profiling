from ydata_profiling.model.modin import utils_modin
from ydata_profiling.model.pandas.describe_timeseries_pandas import (
    pandas_describe_timeseries_1d,
)
from ydata_profiling.model.summary_algorithms import describe_timeseries_1d

modin_describe_timeseries_1d = utils_modin.register(
    describe_timeseries_1d, pandas_describe_timeseries_1d
)
