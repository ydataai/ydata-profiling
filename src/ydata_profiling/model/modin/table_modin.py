from ydata_profiling.model.modin import utils_modin
from ydata_profiling.model.pandas.table_pandas import pandas_get_table_stats
from ydata_profiling.model.table import get_table_stats

modin_get_table_stats = utils_modin.register(get_table_stats, pandas_get_table_stats)
