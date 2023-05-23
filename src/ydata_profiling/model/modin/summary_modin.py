"""Compute statistical description of datasets."""


from tqdm import tqdm
from visions import VisionsTypeset

from ydata_profiling.config import Settings
from ydata_profiling.model.pandas.summary_pandas import (
    pandas_describe_1d,
    pandas_get_series_descriptions,
)
from ydata_profiling.model.summarizer import BaseSummarizer
from ydata_profiling.model.summary import describe_1d, get_series_descriptions
from ydata_profiling.utils import modin


@describe_1d.register
def modin_describe_1d(
    config: Settings,
    series: modin.Series,
    summarizer: BaseSummarizer,
    typeset: VisionsTypeset,
) -> dict:
    return pandas_describe_1d(config, series, summarizer, typeset)


@get_series_descriptions.register
def modin_get_series_descriptions(
    config: Settings,
    df: modin.DataFrame,
    summarizer: BaseSummarizer,
    typeset: VisionsTypeset,
    pbar: tqdm,
) -> dict:
    return pandas_get_series_descriptions(config, df, summarizer, typeset, pbar)
