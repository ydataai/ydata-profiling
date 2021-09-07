from typing import Any, List, TypeVar

from multimethod import multimethod

from pandas_profiling.config import Settings
from pandas_profiling.model.schema import Sample


@multimethod
def get_sample(config: Settings, df: Any) -> List[Sample]:
    raise NotImplementedError()


def get_custom_sample(sample: dict) -> List[Sample]:
    if "name" not in sample:
        sample["name"] = None
    if "caption" not in sample:
        sample["caption"] = None

    samples = [
        Sample(
            id="custom",
            data=sample["data"],
            name=sample["name"],
            caption=sample["caption"],
        )
    ]
    return samples
