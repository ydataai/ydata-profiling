"""Paths that are useful throughout the project."""
from pathlib import Path


def get_project_root() -> Path:
    """Returns the path to the project root folder.

    Returns:
        The path to the project root folder.
    """
    return Path(__file__).parent.parent.parent.parent


def get_config_default() -> Path:
    """Returns the path to the default config file.

    Returns:
        The path to the default config file.
    """
    return Path(__file__).parent.parent / "config_default.yaml"


def get_config_minimal() -> Path:
    """Returns the path to the minimal config file.

    Returns:
        The path to the default config file.
    """
    return Path(__file__).parent.parent / "config_minimal.yaml"


def get_data_path() -> Path:
    return get_project_root() / "data"
