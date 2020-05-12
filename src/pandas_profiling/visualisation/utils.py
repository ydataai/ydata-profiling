"""Plotting utility functions."""
import base64
import uuid
from io import BytesIO, StringIO
from pathlib import Path
from typing import Tuple, Union
from urllib.parse import quote

from pandas_profiling.config import config


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


def base64_image(image: bytes, mime_type: str):
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


def plot_360_n0sc0pe(plt, image_format: Union[str, None] = None, attempts=0) -> str:
    """Quickscope the plot to a base64 encoded string.

    Args:
        image_format: png or svg, overrides config.
        plt: The pyplot module.
        attempts: number to tries

    Returns:
        A base64 encoded version of the plot in the specified image format.
    """

    if image_format is None:
        image_format = config["plot"]["image_format"].get(str)
    if image_format not in ["svg", "png"]:
        raise ValueError('Can only 360 n0sc0pe "png" or "svg" format.')

    inline = config["html"]["inline"].get(bool)

    mime_types = {"png": "image/png", "svg": "image/svg+xml"}

    try:
        if inline:
            if image_format == "svg":
                image_str = StringIO()
                plt.savefig(image_str, format=image_format)
                image_str.seek(0)
                result_string = image_str.getvalue()
            else:
                image_bytes = BytesIO()
                plt.savefig(
                    image_bytes, dpi=config["plot"]["dpi"].get(int), format=image_format
                )
                image_bytes.seek(0)
                result_string = base64_image(
                    image_bytes.getvalue(), mime_types[image_format]
                )
        else:
            file_path = Path(config["html"]["file_name"].get(str))
            suffix = f"_assets/images/{uuid.uuid4().hex}.{image_format}"
            args = {
                "fname": f"{file_path.with_suffix('')}{suffix}",
                "format": image_format,
            }

            if image_format == "png":
                args["dpi"] = config["plot"]["dpi"].get(int)

            plt.savefig(**args)
            result_string = f"{file_path.stem}{suffix}"
        plt.close()
    except RuntimeError:
        plt.close()
        # Hack https://stackoverflow.com/questions/44666207/matplotlib-error-when-running-plotting-in-multiprocess
        # #comment79373127_44666207
        if attempts > 10:
            return ""
        else:
            return plot_360_n0sc0pe(plt, image_format, attempts + 1)
    finally:
        plt.close("all")

    return result_string
