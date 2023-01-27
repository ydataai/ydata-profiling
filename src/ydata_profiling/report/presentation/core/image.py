from typing import Any, Optional

from ydata_profiling.config import ImageType
from ydata_profiling.report.presentation.core.item_renderer import ItemRenderer


class Image(ItemRenderer):
    def __init__(
        self,
        image: str,
        image_format: ImageType,
        alt: str,
        caption: Optional[str] = None,
        **kwargs,
    ):
        if image is None:
            raise ValueError(f"Image may not be None (alt={alt}, caption={caption})")

        super().__init__(
            "image",
            {
                "image": image,
                "image_format": image_format,
                "alt": alt,
                "caption": caption,
            },
            **kwargs,
        )

    def __repr__(self) -> str:
        return "Image"

    def render(self) -> Any:
        raise NotImplementedError()
