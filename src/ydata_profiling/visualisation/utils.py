"""Plotting utility functions."""
import base64
import uuid
from io import BytesIO, StringIO
from pathlib import Path
from typing import List, Optional, Tuple
from urllib.parse import quote

import matplotlib.pyplot as plt
from matplotlib.artist import Artist

from ydata_profiling.config import Settings


def hex_to_rgb(hex: str) -> Tuple[float, ...]:
    """Format a hex value (#FFFFFF) as normalized RGB (1.0, 1.0, 1.0).

    Args:
        hex: The hex value.

    Returns:
        The RGB representation of that hex color value.
    """
    hex = hex.lstrip("#")
    hlen = len(hex)
    return tuple(
        int(hex[i : i + hlen // 3], 16) / 255 for i in range(0, hlen, hlen // 3)
    )


def base64_image(image: bytes, mime_type: str) -> str:
    """Encode the image for an URL using base64

    Args:
        image: the image
        mime_type: the mime type

    Returns:
        A string starting with "data:{mime_type};base64,"
    """
    base64_data = base64.b64encode(image)
    image_data = quote(base64_data)
    return f"data:{mime_type};base64,{image_data}"


def plot_360_n0sc0pe(
    config: Settings,
    image_format: Optional[str] = None,
    bbox_extra_artists: Optional[List[Artist]] = None,
    bbox_inches: Optional[str] = None,
) -> str:
    """Quickscope the plot to a base64 encoded string.

    Args:
        config: Settings
        image_format: png or svg, overrides config.

    Returns:
        A base64 encoded version of the plot in the specified image format.
    """

    if image_format is None:
        image_format = config.plot.image_format.value

    mime_types = {"png": "image/png", "svg": "image/svg+xml"}
    if image_format not in mime_types:
        raise ValueError('Can only 360 n0sc0pe "png" or "svg" format.')

    if config.html.inline:
        if image_format == "svg":
            image_str = StringIO()

            plt.savefig(
                image_str,
                format=image_format,
                bbox_extra_artists=bbox_extra_artists,
                bbox_inches=bbox_inches,
            )
            plt.close()
            result_string = image_str.getvalue()
        else:
            image_bytes = BytesIO()
            plt.savefig(
                image_bytes,
                dpi=config.plot.dpi,
                format=image_format,
                bbox_extra_artists=bbox_extra_artists,
                bbox_inches=bbox_inches,
            )
            plt.close()
            result_string = base64_image(
                image_bytes.getvalue(), mime_types[image_format]
            )
    else:
        if config.html.assets_path is None:
            raise ValueError("config.html.assets_path may not be none")

        file_path = Path(config.html.assets_path)
        suffix = f"{config.html.assets_prefix}/images/{uuid.uuid4().hex}.{image_format}"
        args = {
            "fname": file_path / suffix,
            "format": image_format,
        }

        if image_format == "png":
            args["dpi"] = config.plot.dpi
        plt.savefig(
            bbox_extra_artists=bbox_extra_artists, bbox_inches=bbox_inches, **args
        )
        plt.close()
        result_string = suffix

    return result_string
