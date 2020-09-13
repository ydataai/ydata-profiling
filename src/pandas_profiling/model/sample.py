import attr
import pandas as pd

from pandas_profiling.config import config


@attr.s
class Sample(object):
    id = attr.ib()
    data = attr.ib()
    name = attr.ib()
    caption = attr.ib(default=None)


def get_sample(df: pd.DataFrame) -> list:
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

    n_tail = config["samples"]["tail"].get(int)
    if n_tail > 0:
        samples.append(Sample("tail", df.tail(n=n_tail), "Last rows"))

    n_random = config["samples"]["random"].get(int)
    if n_random > 0:
        samples.append(Sample("random", df.sample(n=n_random), "Random sample"))

    return samples
