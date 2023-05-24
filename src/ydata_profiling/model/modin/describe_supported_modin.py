from ydata_profiling.model.modin import utils_modin
from ydata_profiling.model.pandas.describe_supported_pandas import (
    pandas_describe_supported,
)
from ydata_profiling.model.summary_algorithms import describe_supported

modin_describe_supported = utils_modin.register(
    describe_supported, pandas_describe_supported
)
