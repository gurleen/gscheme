"""
parse.py
gurleen singh<gs585@drexel.edu>
"""
from typing import List as ListType


Symbol = str
List = list
Number = (int, float)
Atom = (Symbol, Number)
Expr = (Atom, List)


def tokenize(chars: str) -> ListType[str]:
    """Returns the program as a list of tokens (including parenthesis)."""
    return chars.replace("(", " ( ").replace(")", " ) ").split()


def make_atom(token: str) -> Atom:
    """Turns the given token into an Atom type."""
    try:
        return int(token)
    except ValueError:
        try:
            return float(token)
        except ValueError:
            return Symbol(token)


def lexer(tokens: ListType[str]) -> Expr:
    """Generates abstract syntax tree from list of tokens."""
    token = tokens.pop(0)
    if token == "(":
        L = []
        while tokens[0] != ")":
            L.append(lexer(tokens))
        tokens.pop(0)
        return L
    elif token == ")":
        raise SyntaxError("Unexpected )")
    else:
        return make_atom(token)


def parse(program: str) -> Expr:
    """Runs both tokenizer and lexer."""
    return lexer(tokenize(program))


if __name__ == '__main__':
    print(lexer(tokenize("(begin (define r 10) (* pi (* r r)))")))
