from ydata_profiling.model.modin import utils_modin
from ydata_profiling.model.pandas.sample_pandas import pandas_get_sample
from ydata_profiling.model.sample import get_sample

modin_get_sample = utils_modin.register(get_sample, pandas_get_sample)
