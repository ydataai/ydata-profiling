from ydata_profiling.model.modin import utils_modin
from ydata_profiling.model.pandas.describe_boolean_pandas import (
    pandas_describe_boolean_1d,
)
from ydata_profiling.model.summary_algorithms import describe_boolean_1d

modin_describe_boolean_1d = utils_modin.register(
    describe_boolean_1d, pandas_describe_boolean_1d
)
