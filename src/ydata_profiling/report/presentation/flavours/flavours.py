"""
    Flavours registry information
"""
from typing import Callable, Dict, Type

from ydata_profiling.report.presentation.core import Root
from ydata_profiling.report.presentation.core.renderable import Renderable

_FLAVOUR_REGISTRY: Dict[str, Dict[Type[Renderable], Type[Renderable]]] = {}


def register_flavour(name: str, mapping: Dict[Type[Renderable], Type[Renderable]]) -> None:
    """Register a flavour mapping.
    
    :param name: The flavour name
    :param mapping: Dictionary mapping core renderable types to flavour-specific types
    """
    _FLAVOUR_REGISTRY[name] = mapping


def get_flavour_mapping(name: str) -> Dict[Type[Renderable], Type[Renderable]]:
    """Get a registered flavour mapping.
    
    :param name: The flavour name
    :return: The flavour mapping dictionary
    :raises ValueError: If the flavour is not registered
    """
    if name not in _FLAVOUR_REGISTRY:
        raise ValueError(f"Flavour '{name}' is not registered.")
    return _FLAVOUR_REGISTRY[name]


def apply_renderable_mapping(
    mapping: Dict[Type[Renderable], Type[Renderable]],
    structure: Renderable,
    flavour_func: Callable[[Renderable], None],
) -> None:
    """Apply flavour mapping to a renderable structure.
    
    :param mapping: The flavour mapping dictionary
    :param structure: The renderable structure to transform
    :param flavour_func: The flavour application function for recursive calls
    """
    mapping[type(structure)].convert_to_class(structure, flavour_func)


def HTMLReport(structure: Root) -> Root:
    from ydata_profiling.report.presentation.flavours import flavour_html  # noqa: F401

    mapping = get_flavour_mapping("html")
    apply_renderable_mapping(mapping, structure, flavour_func=HTMLReport)
    return structure


def WidgetReport(structure: Root) -> Root:
    from ydata_profiling.report.presentation.flavours import (  # noqa: F401
        flavour_widget,
    )

    mapping = get_flavour_mapping("widget")
    apply_renderable_mapping(mapping, structure, flavour_func=WidgetReport)
    return structure
