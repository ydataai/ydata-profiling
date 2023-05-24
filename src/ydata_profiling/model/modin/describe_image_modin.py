from ydata_profiling.model.modin import utils_modin
from ydata_profiling.model.pandas.describe_image_pandas import pandas_describe_image_1d
from ydata_profiling.model.summary_algorithms import describe_image_1d
from ydata_profiling.utils.imghdr_patch import *  # noqa: F401,F403

modin_describe_image_1d = utils_modin.register(
    describe_image_1d, pandas_describe_image_1d
)
