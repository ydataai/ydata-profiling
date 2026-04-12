"""
    Flavours registry information
"""
from typing import Callable, Dict, Type

from ydata_profiling.report.presentation.core import Root
from ydata_profiling.report.presentation.core.renderable import Renderable

_FlavourMapping = Dict[Type[Renderable], Type[Renderable]]
_FLAVOUR_REGISTRY: Dict[str, _FlavourMapping] = {}


def register_flavour(name: str, mapping: _FlavourMapping) -> None:
    _FLAVOUR_REGISTRY[name] = mapping


def get_flavour_mapping(name: str) -> _FlavourMapping:
    if name not in _FLAVOUR_REGISTRY:
        raise ValueError(f"Flavour '{name}' is not registered.")
    return _FLAVOUR_REGISTRY[name]


_FlavourFunc = Callable[[Renderable], Renderable]


def apply_renderable_mapping(
    mapping: _FlavourMapping,
    structure: Renderable,
    flavour_func: _FlavourFunc,
) -> None:
    mapping[type(structure)].convert_to_class(structure, flavour_func)


def HTMLReport(structure: Root) -> Root:
    from ydata_profiling.report.presentation.flavours import flavour_html  # noqa: F401

    mapping = get_flavour_mapping("html")
    apply_renderable_mapping(mapping, structure, flavour_func=HTMLReport)  # type: ignore
    return structure


def WidgetReport(structure: Root) -> Root:
    from ydata_profiling.report.presentation.flavours import (  # noqa: F401
        flavour_widget,
    )

    mapping = get_flavour_mapping("widget")
    apply_renderable_mapping(mapping, structure, flavour_func=WidgetReport)  # type: ignore
    return structure
