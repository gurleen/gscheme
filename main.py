"""
a scheme interpreter
gurleen singh<gs585@drexel.edu>
"""
from env import std_env, Env
from parser import Expr, parse, Symbol, List


global_env = std_env()


class Procedure(object):
    "A user-defined Scheme procedure."
    def __init__(self, parms, body, env):
        self.parms, self.body, self.env = parms, body, env

    def __call__(self, *args): 
        return eval(self.body, Env(self.parms, args, self.env))


def eval(x: Expr, env=global_env) -> Expr:
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
        exp = (conseq if eval(cond, env) else alt)
        return eval(exp, env)
    elif op == "define":
        (_, symbol, exp) = x
        env[symbol] = eval(exp, env)
    elif op == "set!":
        (symbol, exp) = args
        env.find(symbol)[symbol] = eval(exp, env)
    elif op == "lambda":
        (params, body) = args
        return Procedure(params, body, env)
    else:
        proc = eval(op, env)
        args = [eval(arg, env) for arg in args]
        return proc(*args)


def repl():
    """Provides a basic REPL."""
    while True:
        try:
            x = input("> ")
            if not x: continue
            rv = eval(parse(x))
            if rv is not None: print(rv)
        except KeyboardInterrupt:
            print("\nExiting...")
            quit()
        except Exception as e:
            print("Interpreter error:", e)


def main():
    print("gscheme")
    print("press ctrl+c to exit")
    repl()


if __name__ == '__main__':
    main()
