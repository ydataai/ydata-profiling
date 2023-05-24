from ydata_profiling.model.missing import missing_bar, missing_heatmap, missing_matrix
from ydata_profiling.model.modin import utils_modin
from ydata_profiling.model.pandas.missing_pandas import (
    pandas_missing_bar,
    pandas_missing_heatmap,
    pandas_missing_matrix,
)

modin_missing_bar = utils_modin.register(missing_bar, pandas_missing_bar)
modin_missing_matrix = utils_modin.register(missing_matrix, pandas_missing_matrix)
modin_missing_heatmap = utils_modin.register(missing_heatmap, pandas_missing_heatmap)
