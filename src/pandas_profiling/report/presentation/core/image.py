from typing import Any

from pandas_profiling.report.presentation.core.item_renderer import ItemRenderer


class Image(ItemRenderer):
    def __init__(self, image, image_format, alt, caption=None, **kwargs):
        super().__init__(
            "image",
            {
                "image": image,
                "image_format": image_format,
                "alt": alt,
                "caption": caption,
            },
            **kwargs
        )

    def __repr__(self):
        return "Image"

    def render(self) -> Any:
        raise NotImplementedError()
