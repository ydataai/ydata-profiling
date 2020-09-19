import logging
from functools import partial, singledispatch
from typing import Any, Callable, Union

from pandas_profiling.config import config
from pandas_profiling.report.presentation.core.renderable import Renderable

logging.basicConfig(level=logging.INFO)
current_backend = config["plot"]["backend"].get(str)


class PlotRegister:
    data = {}
    logger = logging.getLogger(__name__)

    @classmethod
    def register(cls, mod_name=None):
        def decorator(fn, mod_name=None):
            if mod_name is None:
                mod_name = fn.__module__.split(".")[-1]
            cls.data[(mod_name, fn.__name__)] = fn
            return fn

        return partial(decorator, mod_name=mod_name)

    @classmethod
    def get_fn(cls, backend, function_name: str):
        cls.logger.info(f"{function_name} using {backend}")
        return cls.data.get((f"{backend}_", function_name), None)


def plot_entry(fn: Union[Callable, str]):
    def inner(*args, **kwargs):
        real_fn = PlotRegister.get_fn(current_backend, fn.__name__)
        if real_fn is None:
            real_fn = fn
        return real_fn(*args, **kwargs)

    return inner


@plot_entry
def pie_chart(data: Any):
    raise NotImplementedError


@plot_entry
def histogram(data: Any):
    raise NotImplementedError


@plot_entry
def qq_plot(data: Any, distribution="normal"):
    raise NotImplementedError


@plot_entry
def correlation_matrix(plot_obj: Any, *args, **kwargs):
    raise NotImplementedError


@plot_entry
def bar(plot_obj: Any):
    raise NotImplementedError


@plot_entry
def scatter(plot_obj: Any):
    raise NotImplementedError


@plot_entry
def scatter_series(plot_obj: Any):
    raise NotImplementedError


@plot_entry
def scatter_complex(plot_obj: Any):
    raise NotImplementedError


@plot_entry
def heatmap(plot_obj: Any):
    raise NotImplementedError


@plot_entry
def boxplot(plot_obj: Any):
    raise NotImplementedError


@plot_entry
def missing_bar(plot_obj: Any):
    raise NotImplementedError


@plot_entry
def missing_heatmap(plot_obj: Any):
    raise NotImplementedError


@plot_entry
def missing_dendrogram(plot_obj: Any):
    raise NotImplementedError


@plot_entry
def missing_matrix(plot_obj: Any):
    raise NotImplementedError


@singledispatch
def render_plot(plot_obj: Any, *args, **kwargs) -> Renderable:
    raise NotImplementedError


@plot_entry
def kde(plot_obj: Any):
    raise NotImplementedError
