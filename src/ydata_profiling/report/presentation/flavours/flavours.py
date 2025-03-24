"""
    Flavours registry information
"""
from ydata_profiling.report.presentation.core import Root

from typing import Dict, Type
from ydata_profiling.report.presentation.core.renderable import Renderable


_FLAVOUR_REGISTRY: Dict[str, Dict[Renderable, Renderable]] = {}

def register_flavour(name: str, mapping: Dict[Renderable, Renderable]) -> None:
    _FLAVOUR_REGISTRY[name] = mapping

def get_flavour_mapping(name: str) -> Dict[Renderable, Renderable]:
    if name not in _FLAVOUR_REGISTRY:
        raise ValueError(f"Flavour '{name}' is not registered.")
    return _FLAVOUR_REGISTRY[name]

def apply_renderable_mapping(
    mapping: Dict[Renderable, Renderable],
    structure: Renderable,
    flavour_func: Root,
) -> None:
    mapping[type(structure)].convert_to_class(structure, flavour_func)

def HTMLReport(structure: Root) -> Root:
    from ydata_profiling.report.presentation.flavours import flavour_html # noqa: F401

    mapping = get_flavour_mapping("html")
    apply_renderable_mapping(mapping, structure, flavour_func=HTMLReport)
    return structure

def WidgetReport(structure: Root) -> Root:
    from ydata_profiling.report.presentation.flavours import flavour_widget # noqa: F401

    mapping = get_flavour_mapping("widget")
    apply_renderable_mapping(mapping, structure, flavour_func=WidgetReport)
    return structure