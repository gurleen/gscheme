"""
env.py
gurleen singh<gs585@drexel.edu>
"""

import json
import math
import operator as op

from parser import List, Number, Symbol
from stdlib.net import net_functions
from stdlib.file import file_functions


class Env(dict):
    def __init__(self, parms=(), args=(), outer=None):
        self.update(zip(parms, args))
        self.outer = outer

    def find(self, var):
        "Find the innermost Env where var appears."
        return self if (var in self) else self.outer.find(var)


class SchemeError(Exception):
    pass


def raise_exception(x: str):
    raise SchemeError(x)


def std_env() -> Env:
    """Prepares a basic environment object with all builtin functions."""
    env = Env()
    env.update(vars(math))
    env.update(
        {
            "+": op.add,
            "-": op.sub,
            "*": op.mul,
            "/": op.truediv,
            ">": op.gt,
            "<": op.lt,
            ">=": op.ge,
            "<=": op.le,
            "=": op.eq,
            "abs": abs,
            "append": op.add,
            "apply": lambda proc, args: proc(*args),
            "begin": lambda *x: x[-1],
            "car": lambda x: x[0],
            "cdr": lambda x: x[1:],
            "cons": lambda x, y: [x] + y,
            "eq?": op.is_,
            "expt": pow,
            "equal?": op.eq,
            "length": len,
            "list": List,
            "list?": lambda x: isinstance(x, List),
            "map": lambda f, s: list(map(f, s)),
            "max": max,
            "min": min,
            "not": op.not_,
            "null?": lambda x: x == [],
            "number?": lambda x: isinstance(x, Number),
            "display": lambda *x: print(*x, end=""),
            "displayln": print,
            "procedure?": callable,
            "round": round,
            "symbol?": lambda x: isinstance(x, Symbol),
            "error": raise_exception,
            "exit": lambda: quit(),
            "newline": lambda: print(),
            "str-format": lambda x, *y: x.format(*y),
            "str-split": lambda x, y: x.split(y),
            "json-parse": json.loads,
            "json-encode": json.dumps,
            **net_functions,
            **file_functions
        }
    )
    return env
