from functools import reduce
from typing import Callable, Dict, List

import networkx as nx
from visions import VisionsTypeset


def compose(functions):
    """
    Compose a sequence of functions
    :param functions: sequence of functions
    :return: combined functions, e.g. [f(x), g(x)] -> g(f(x))
    """

    def func(f: Callable, g: Callable):
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
        mapping: Dict[str, List[Callable]],
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
            self.mapping[str(to_type)] = (
                self.mapping[str(from_type)] + self.mapping[str(to_type)]
            )

    def handle(self, dtype: str, *args, **kwargs) -> dict:
        """

        Returns:
            object:
        """
        funcs = self.mapping.get(dtype, [])
        op = compose(funcs)
        return op(*args)


def get_render_map():
    import pandas_profiling.report.structure.variables as render_algorithms

    render_map = {
        "Boolean": render_algorithms.render_boolean,
        "Numeric": render_algorithms.render_real,
        "Complex": render_algorithms.render_complex,
        "DateTime": render_algorithms.render_date,
        "Categorical": render_algorithms.render_categorical,
        "URL": render_algorithms.render_url,
        "Path": render_algorithms.render_path,
        "File": render_algorithms.render_file,
        "Image": render_algorithms.render_image,
        "Unsupported": render_algorithms.render_generic,
    }

    return render_map
