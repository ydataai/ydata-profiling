from ydata_profiling.model.modin import utils_modin
from ydata_profiling.model.pandas.describe_numeric_pandas import (
    pandas_describe_numeric_1d,
)
from ydata_profiling.model.summary_algorithms import describe_numeric_1d

modin_describe_numeric_1d = utils_modin.register(
    describe_numeric_1d, pandas_describe_numeric_1d
)
