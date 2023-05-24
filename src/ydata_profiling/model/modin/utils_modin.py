import typing
from types import FunctionType
from typing import Callable, Dict, Type

import pandas as pd
from multimethod import multimethod

from ydata_profiling.utils import modin

MODIN_EQUIV = {pd.DataFrame: modin.DataFrame, pd.Series: modin.Series}


def _to_modin_typing_info(typing_info: Dict[str, Type]) -> Dict[str, Type]:
    "Convert an annotation dict containing pandas to modin."
    new_info = {}

    for arg, typ in typing_info.items():
        new_info[arg] = MODIN_EQUIV.get(typ, typ)

    return new_info


def _to_modin_type_hints(pd_func: Callable) -> Callable:
    "Convert pandas function to modin."
    modin_func = FunctionType(
        pd_func.__code__,
        pd_func.__globals__,
        pd_func.__name__.replace("pandas", "modin"),
        pd_func.__defaults__,
        pd_func.__closure__,
    )
    modin_func.__doc__ = pd_func.__doc__
    modin_func.__annotations__ = _to_modin_typing_info(typing.get_type_hints(pd_func))
    return modin_func


def register(func: multimethod, pd_func: Callable) -> Callable:
    """
    Registers a modin version of the pandas function into the multimethod.

    Parameters
    ----------

    func: multimethod
        The function to dispatch

    pd_func: Callable
        The pandas function that backs the multimethod.

    Returns
    -------

    A wrapped function. It has modin in its typing information but uses the pandas function to execute the inputs.
    """
    modin_func = _to_modin_type_hints(pd_func)
    return func.register(modin_func)
