"""
    Auxiliary handler methods for data summary extraction
"""
from typing import Any, Callable, Dict, List, Sequence, Tuple, TypeVar, cast

import networkx as nx
from visions import VisionsTypeset

T = TypeVar("T")
SummaryFunction = Callable[..., Tuple[Any, ...]]


def compose(functions: Sequence[SummaryFunction]) -> SummaryFunction:
    """
    Compose a sequence of functions.

    :param functions: sequence of functions
    :return: combined function applying all functions in order.
    """

    def composed_function(*args: Any) -> Tuple[Any, ...]:
        result: Tuple[Any, ...] = args
        for func in functions:
            step_result = func(*result)
            if not isinstance(step_result, tuple):
                result = (step_result,)
            else:
                result = step_result
        return result

    return composed_function


class Handler:
    """A generic handler

    Allows any custom mapping between data types and functions
    """

    def __init__(
        self,
        mapping: Dict[str, List[SummaryFunction]],
        typeset: VisionsTypeset,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        self.mapping: Dict[str, List[SummaryFunction]] = mapping
        self.typeset = typeset
        self._complete_dag()

    def _complete_dag(self) -> None:
        for from_type, to_type in nx.topological_sort(
            nx.line_graph(self.typeset.base_graph)
        ):
            from_type_str = str(from_type)
            to_type_str = str(to_type)
            
            if from_type_str not in self.mapping:
                continue
                
            if to_type_str in self.mapping:
                self.mapping[to_type_str] = (
                    self.mapping[from_type_str] + self.mapping[to_type_str]
                )
            else:
                self.mapping[to_type_str] = self.mapping[from_type_str].copy()

    def handle(self, dtype: str, *args: Any, **kwargs: Any) -> Dict[str, Any]:
        """
        Returns:
            object: a tuple containing the config, the dataset series and the summary extracted
        """
        funcs = self.mapping.get(dtype, [])
        op = compose(funcs)
        result = op(*args)
        return cast(Dict[str, Any], result[-1])


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
