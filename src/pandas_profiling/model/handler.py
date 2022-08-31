from typing import Callable, Dict, List

import networkx as nx
from visions import VisionsTypeset

from pandas_profiling.model.schema import ColumnResult


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

    def _complete_dag(self) -> None:
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
        results = {"type": dtype}
        for i, fnx in enumerate(funcs):
            cfg, series, res = fnx(*args, results, **kwargs)
            results[fnx.__name__] = res
            if type(res) != bool:
                args = (cfg, series)

        complete = [
            res.dict() if isinstance(res, ColumnResult) else {k: res}
            for k, res in results.items()
        ]

        resz = {}
        for v in complete:
            resz.update(v)

        return resz


def get_render_map() -> Dict[str, Callable]:
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
        "TimeSeries": render_algorithms.render_timeseries,
    }

    return render_map
