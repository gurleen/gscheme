"""
parse.py
gurleen singh<gs585@drexel.edu>
"""
import re
from typing import List as ListType


class Symbol(str):
    pass


List = list
Number = (int, float)
Atom = (Symbol, Number)
Expr = (Atom, List)


eof_object = Symbol('#<eof-object>')


class InPort:
    tokenizer = r'''\s*(,@|[('`,)]|"(?:[\\].|[^\\"])*"|;.*|[^\s('"`,;)]*)(.*)'''

    def __init__(self, file_obj):
        self.file = file_obj
        self.line = ""

    def next_token(self):
        while True:
            if self.line == "":
                self.line = self.file.readline()
            if self.line == "":
                return eof_object
            token, self.line = re.match(InPort.tokenizer, self.line).groups()
            if token != "" and not token.startswith(";"):
                return token


def get_or_create_symbol(s, symbol_table={}) -> Symbol:
    if s not in symbol_table:
        symbol_table[s] = Symbol(s)
    return symbol_table[s]


_quote, _if, _set, _define, _lambda, _begin, _definemacro, = map(
    get_or_create_symbol,
    "quote   if   set!  define   lambda   begin   define-macro".split(),
)

_quasiquote, _unquote, _unquotesplicing = map(
    get_or_create_symbol, "quasiquote   unquote   unquote-splicing".split()
)

quotes = {"'": _quote, "`": _quasiquote, ",": _unquote, ",@": _unquotesplicing}


def read_char(inport: InPort) -> Symbol:
    if inport.line != "":
        ch, inport.line = inport.line[0], inport.line[1:]
        return ch
    else:
        return inport.file.read(1) or eof_object


def read(inport: InPort):
    def read_ahead(token):
        if token == "(":
            L = []
            while True:
                token = inport.next_token()
                if token == ")":
                    return L
                else:
                    L.append(read_ahead(token))
        elif token == ")":
            raise SyntaxError("Unexpected )")
        elif token in quotes:
            return [quotes[token], read(inport)]
        elif token is eof_object:
            raise SyntaxError("Unexpected EOF")
        else:
            return make_atom(token)

    first_token = inport.next_token()
    return eof_object if first_token is eof_object else read_ahead(first_token)


def tokenize(chars: str) -> ListType[str]:
    """Returns the program as a list of tokens (including parenthesis)."""
    return chars.replace("(", " ( ").replace(")", " ) ").split()


def make_atom(token: str) -> Atom:
    """Turns the given token into an Atom type."""
    if token == "#t": return True
    elif token == "#f": return False
    elif token[0] == '"': return token[1:-1]
    try:
        return int(token)
    except ValueError:
        try:
            return float(token)
        except ValueError:
            try:
                return complex(token.replace("i", "j", 1))
            except ValueError:
                return get_or_create_symbol(token)


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


if __name__ == "__main__":
    print(lexer(tokenize("(begin (define r 10) (* pi (* r r)))")))
