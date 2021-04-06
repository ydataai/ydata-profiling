from typing import List, Optional, TypeVar

import pandas as pd
from pydantic.main import BaseModel

from pandas_profiling.config import Settings

PandasDataFrame = TypeVar("pandas.core.frame.DataFrame")  # type: ignore


class Sample(BaseModel):
    id: str
    data: PandasDataFrame  # type: ignore
    name: str
    caption: Optional[str] = None


def get_sample(config: Settings, df: pd.DataFrame) -> List[Sample]:
    """Obtains a sample from head and tail of the DataFrame

    Args:
        config: Settings object
        df: the pandas DataFrame

    Returns:
        a list of Sample objects
    """
    samples: List[Sample] = []
    if len(df) == 0:
        return samples

    n_head = config.samples.head
    if n_head > 0:
        samples.append(Sample(id="head", data=df.head(n=n_head), name="First rows"))

    n_tail = config.samples.tail
    if n_tail > 0:
        samples.append(Sample(id="tail", data=df.tail(n=n_tail), name="Last rows"))

    n_random = config.samples.random
    if n_random > 0:
        samples.append(
            Sample(id="random", data=df.sample(n=n_random), name="Random sample")
        )

    return samples
