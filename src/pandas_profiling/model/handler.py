from functools import reduce
from typing import Callable, Dict, List, Type

import networkx as nx
from visions import VisionsBaseType, VisionsTypeset

from pandas_profiling.model import typeset as ppt


def compose(functions):
    """
    Compose a sequence of functions
    :param functions: sequence of functions
    :return: combined functions, e.g. [f(x), g(x)] -> g(f(x))
    """

    def func(f, g):
        def func2(*x):
            res = g(*x)
            if type(res) == bool:
                return f(*x)
            else:
                return f(*res)

        return func2

    return reduce(func, reversed(functions), lambda *x: x)


class Handler:
    """A generic handler

    Allows any custom mapping between data types and functions
    """

    def __init__(
        self,
        mapping: Dict[Type[VisionsBaseType], List[Callable]],
        typeset: VisionsTypeset,
        *args,
        **kwargs
    ):
        self.mapping = mapping
        self.typeset = typeset

        self._complete_dag()

    def _complete_dag(self):
        for from_type, to_type in nx.topological_sort(
            nx.line_graph(self.typeset.base_graph)
        ):
            self.mapping[to_type] = self.mapping[from_type] + self.mapping[to_type]

    def handle(self, dtype: Type[VisionsBaseType], *args, **kwargs) -> dict:
        """

        Returns:
            object:
        """
        op = compose(self.mapping.get(dtype, []))
        return op(*args)


def get_render_map():
    import pandas_profiling.report.structure.variables as render_algorithms

    render_map = {
        ppt.Boolean: render_algorithms.render_boolean,
        ppt.Numeric: render_algorithms.render_real,
        ppt.Complex: render_algorithms.render_complex,
        ppt.DateTime: render_algorithms.render_date,
        ppt.Categorical: render_algorithms.render_categorical,
        ppt.URL: render_algorithms.render_url,
        ppt.Path: render_algorithms.render_path,
        ppt.File: render_algorithms.render_file,
        ppt.Image: render_algorithms.render_image,
        ppt.Unsupported: render_algorithms.render_generic,
    }

    return render_map
