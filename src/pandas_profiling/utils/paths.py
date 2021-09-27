"""Paths that are useful throughout the project."""
from pathlib import Path


def get_project_root() -> Path:
    """Returns the path to the project root folder.

    Returns:
        The path to the project root folder.
    """
    return Path(__file__).parent.parent.parent.parent


def get_config(file_name: str) -> Path:
    """Returns the path a config file.

    Returns:
        The path to a config file.
    """
    return Path(__file__).parent.parent / file_name


def get_data_path() -> Path:
    """Returns the path to the dataset cache ([root] / data)

    Returns:
        The path to the dataset cache
    """
    return get_project_root() / "data"


def get_html_template_path() -> Path:
    """Returns the path to the HTML templates

    Returns:
        The path to the HTML templates
    """
    return (
        Path(__file__).parent.parent
        / "report"
        / "presentation"
        / "flavours"
        / "html"
        / "templates"
    )
