from ydata_profiling.model.modin import utils_modin
from ydata_profiling.model.pandas.describe_categorical_pandas import (
    pandas_describe_categorical_1d,
)
from ydata_profiling.model.summary_algorithms import describe_categorical_1d

utils_modin.register(describe_categorical_1d, pandas_describe_categorical_1d)
