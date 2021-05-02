from typing import List

from pandas_profiling.config import config
from pandas_profiling.model.dataframe_wrappers import SparkDataFrame
from pandas_profiling.model.sample import Sample


def get_sample_spark(df: SparkDataFrame) -> List[Sample]:
    """Obtains a sample from head and tail of the DataFrame

    Args:
        df: the pandas DataFrame

    Returns:
        a list of Sample objects
    """
    samples = []
    n_head = config["samples"]["head"].get(int)
    if n_head > 0:
        samples.append(Sample("head", df.head(n=n_head), "First rows"))

    n_random = config["samples"]["random"].get(int)
    if n_random > 0:
        samples.append(Sample("random", df.sample, "Random sample"))

    return samples
