from env import std_env, Env
from parser import Expr, Symbol, InPort, read, eof_object


global_env = std_env()
List = list


def load_file(filename: str):
    inport = InPort(open(filename))
    while True:
        exp = read(inport)
        if exp is eof_object:
            break
        evaluated = evaluate(exp)
        if evaluated is not None:
            print(evaluated)


class Procedure(object):
    "A user-defined Scheme procedure."

    def __init__(self, parms, body, env):
        self.parms, self.body, self.env = parms, body, env

    def __call__(self, *args):
        return evaluate(self.body, Env(self.parms, args, self.env))


def evaluate(x: Expr, env=global_env) -> Expr:
    """Evaluate the expression in the given environment."""
    if isinstance(x, Symbol):
        return env.find(x)[x]
    elif not isinstance(x, List):
        return x
    op, *args = x
    if op == "quote":
        return args[0]
    elif op == "if":
        (_, cond, conseq, alt) = x
        exp = conseq if evaluate(cond, env) else alt
        return evaluate(exp, env)
    elif op == "define":
        (_, symbol, exp) = x
        env[symbol] = evaluate(exp, env)
    elif op == "set!":
        (symbol, exp) = args
        env.find(symbol)[symbol] = evaluate(exp, env)
    elif op == "lambda":
        (params, body) = args
        return Procedure(params, body, env)
    elif op == "load":
        load_file(args[0])
    else:
        proc = evaluate(op, env)
        args = [evaluate(arg, env) for arg in args]
        return proc(*args)
