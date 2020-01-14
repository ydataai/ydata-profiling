from typing import Any

from pandas_profiling.report.presentation.abstract.item_renderer import ItemRenderer


class Dataset(ItemRenderer):
    def __init__(
        self,
        package,
        date_start,
        date_end,
        values,
        messages,
        collapse_warnings,
        variables,
        **kwargs
    ):
        super().__init__(
            "dataset",
            {
                "date_start": date_start,
                "date_end": date_end,
                "values": values,
                "messages": messages,
                "variables": variables,
                "collapse_warnings": collapse_warnings,
                "package": package,
            },
            **kwargs
        )

    def render(self) -> Any:
        raise NotImplementedError()
