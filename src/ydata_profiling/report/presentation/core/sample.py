from typing import Any, Optional

import pandas as pd

from ydata_profiling.report.presentation.core.item_renderer import ItemRenderer


class Sample(ItemRenderer):
    def __init__(
        self, name: str, sample: pd.DataFrame, caption: Optional[str] = None, **kwargs
    ):
        super().__init__(
            "sample", {"sample": sample, "caption": caption}, name=name, **kwargs
        )

    def __repr__(self) -> str:
        return "Sample"

    def render(self) -> Any:
        raise NotImplementedError()
