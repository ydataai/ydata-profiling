from typing import List, Optional, TypeVar

from multimethod import multimethod
from pydantic.main import BaseModel

from pandas_profiling.config import Settings

T = TypeVar("T")  # type: ignore


class Sample(BaseModel):
    id: str
    data: T  # type: ignore
    name: str
    caption: Optional[str] = None


@multimethod
def get_sample(config: Settings, df: T) -> List[Sample]:
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
