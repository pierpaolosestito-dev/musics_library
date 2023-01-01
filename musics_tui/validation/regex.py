from typeguard import typechecked
from typing import Callable
import re

@typechecked
def pattern(regex:str) -> Callable:
    r = re.compile(regex)
    def res(value):
        return bool(r.fullmatch(value))
    res.__name__ = f'pattern({regex})'
    return res