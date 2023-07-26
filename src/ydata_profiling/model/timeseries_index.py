"""Compute statistical description of datasets."""

from typing import Any

from multimethod import multimethod


@multimethod
def get_time_index_description(
    df: Any,
    table_stats: dict,
) -> dict:
    raise NotImplementedError()
