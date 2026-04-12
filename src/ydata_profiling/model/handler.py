"""
    Auxiliary handler methods for data summary extraction
"""
from typing import Any, Callable, Dict, List, Sequence, Tuple, Union

import networkx as nx
from visions import VisionsTypeset


def compose(functions: Sequence[Callable]) -> Callable:
    """
    Compose a sequence of functions.

    Each function in the sequence receives the result of the previous function.
    Functions are expected to accept and return tuples for proper chaining.

    :param functions: sequence of functions that accept and return tuples
    :return: combined function applying all functions in order
    """

    def composed_function(*args: Any) -> Tuple[Any, ...]:
        result: Union[Tuple[Any, ...], Any] = args
        for func in functions:
            if isinstance(result, tuple):
                result = func(*result)
            else:
                result = func(result)
        if isinstance(result, tuple):
            return result
        return (result,)

    return composed_function


class Handler:
    """A generic handler

    Allows any custom mapping between data types and functions.
    Functions are composed based on the type hierarchy defined in the typeset.
    """

    def __init__(
        self,
        mapping: Dict[str, List[Callable]],
        typeset: VisionsTypeset,
        *args: Any,
        **kwargs: Any
    ):
        self.mapping = mapping
        self.typeset = typeset
        self._complete_dag()

    def _complete_dag(self) -> None:
        for from_type, to_type in nx.topological_sort(
            nx.line_graph(self.typeset.base_graph)
        ):
            from_key = str(from_type)
            to_key = str(to_type)
            self.mapping[to_key] = self.mapping.get(from_key, []) + self.mapping.get(
                to_key, []
            )

    def handle(self, dtype: str, *args: Any, **kwargs: Any) -> Dict[str, Any]:
        """
        Execute the handler chain for the given data type.

        :param dtype: the data type to handle
        :param args: arguments to pass to the handler functions
        :param kwargs: keyword arguments (currently unused but reserved for extensibility)
        :return: a dictionary containing the summary extracted from the data
        """
        funcs = self.mapping.get(dtype, [])
        op = compose(funcs)
        result = op(*args)
        if result:
            return result[-1] if isinstance(result[-1], dict) else {}
        return {}


def get_render_map() -> Dict[str, Callable]:
    import ydata_profiling.report.structure.variables as render_algorithms

    render_map = {
        "Boolean": render_algorithms.render_boolean,
        "Numeric": render_algorithms.render_real,
        "Complex": render_algorithms.render_complex,
        "Text": render_algorithms.render_text,
        "DateTime": render_algorithms.render_date,
        "Categorical": render_algorithms.render_categorical,
        "URL": render_algorithms.render_url,
        "Path": render_algorithms.render_path,
        "File": render_algorithms.render_file,
        "Image": render_algorithms.render_image,
        "Unsupported": render_algorithms.render_generic,
        "TimeSeries": render_algorithms.render_timeseries,
    }

    return render_map
