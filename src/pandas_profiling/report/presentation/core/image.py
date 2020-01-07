from typing import Any

from pandas_profiling.report.presentation.abstract.item_renderer import ItemRenderer


class Image(ItemRenderer):
    def __init__(self, image, alt, caption=None, **kwargs):
        super().__init__(
            "image", {"image": image, "alt": alt, "caption": caption}, **kwargs
        )

    def render(self) -> Any:
        raise NotImplementedError()
