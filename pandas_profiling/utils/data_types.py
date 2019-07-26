from pathlib import Path


def str_is_path(p: str):
    """Detects if the variable contains absolute paths. If so, we distinguish paths that exist and paths that are images.

    Args:
        p: the Path

    Returns:
        True is is an absolute path
    """
    try:
        path = Path(p)
        if path.is_absolute():
            return True
        else:
            return False
    except TypeError:
        return False
