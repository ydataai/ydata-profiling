import imghdr
from pathlib import Path
from typing import Optional, Tuple, Union

import imagehash
from PIL import ExifTags, Image

from pandas_profiling.model.imghdr_patch import *  # noqa: F401,F403


def open_image(path: Path) -> Optional[Image.Image]:
    """

    Args:
        path:

    Returns:

    """
    try:
        return Image.open(path)
    except (OSError, AttributeError):
        return None


def is_image_truncated(image: Image) -> bool:
    """Returns True if the path refers to a truncated image

    Args:
        image:

    Returns:
        True if the image is truncated
    """
    try:
        image.load()
        return False
    except (OSError, AttributeError):
        return True


def get_image_shape(image: Image) -> Optional[Tuple[int, int]]:
    """

    Args:
        image:

    Returns:

    """
    try:
        return image.size
    except (OSError, AttributeError):
        return None


def hash_image(image: Image) -> Optional[str]:
    """

    Args:
        image:

    Returns:

    """
    try:
        return str(imagehash.phash(image))
    except (OSError, AttributeError):
        return None


def decode_byte_exif(exif_val: Union[str, bytes]) -> str:
    """Decode byte encodings

    Args:
        exif_val:

    Returns:

    """
    if isinstance(exif_val, str):
        return exif_val
    else:
        return exif_val.decode()


def extract_exif(image: Image) -> dict:
    """

    Args:
        image:

    Returns:

    """
    try:
        exif_data = image._getexif()
        if exif_data is not None:
            exif = {
                ExifTags.TAGS[k]: decode_byte_exif(v)
                for k, v in exif_data.items()
                if k in ExifTags.TAGS
            }
        else:
            exif = {}
    except (AttributeError, OSError):
        # Not all file types (e.g. .gif) have exif information.
        exif = {}

    return exif


def path_is_image(p: Path) -> bool:
    return imghdr.what(p) is not None
