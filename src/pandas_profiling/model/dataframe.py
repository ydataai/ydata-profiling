from typing import Any

from multimethod import multimethod


@multimethod
def check_dataframe(df: Any) -> None:
    raise NotImplementedError()


@multimethod
def preprocess(df: Any) -> Any:
    return df
