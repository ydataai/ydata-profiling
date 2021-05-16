from functools import wraps
from typing import Any, Callable

from tqdm import tqdm


def progress(fn: Callable, bar: tqdm, message: str) -> Callable:
    @wraps(fn)
    def inner(*args, **kwargs) -> Any:
        bar.set_postfix_str(message)
        ret = fn(*args, **kwargs)
        bar.update()
        return ret

    return inner
