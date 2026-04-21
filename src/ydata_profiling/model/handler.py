"""
    Auxiliary handler methods for data summary extraction
"""
from typing import Any, Callable, Dict, List, Sequence

import networkx as nx
from visions import VisionsTypeset


def compose(functions: Sequence[Callable]) -> Callable:
    """
    Compose a sequence of functions.

    :param functions: sequence of functions
    :return: combined function applying all functions in order.
    """

    def composed_function(*args) -> List[Any]:
        result = args  # Start with the input arguments
        for func in functions:
            result = func(*result) if isinstance(result, tuple) else func(result)
        return result  # type: ignore

    return composed_function  # type: ignore


class Handler:
    """Generic handler for data type specific processing pipelines.

    Builds a processing pipeline for each data type by composing functions
    along the type hierarchy. Allows custom summarization strategies.
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

    def _complete_dag(self) -> None:
        """Propagate functions along the type hierarchy DAG.

        Functions defined for parent types are inherited by subtypes,
        creating a complete processing pipeline for each type.
        """
        for from_type, to_type in nx.topological_sort(
            nx.line_graph(self.typeset.base_graph)
        ):
            self.mapping[str(to_type)] = (
                self.mapping[str(from_type)] + self.mapping[str(to_type)]
            )

    def handle(self, dtype: str, *args, **kwargs) -> dict:
        """Execute the processing pipeline for a given data type.

        Args:
            dtype: Name of the data type to process
            *args: Arguments passed to the processing pipeline
            **kwargs: Additional keyword arguments

        Returns:
            Extracted summary dictionary
        """
        funcs = self.mapping.get(dtype, [])
        op = compose(funcs)
        summary = op(*args)[-1]
        return summary
