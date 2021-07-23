"""
a scheme interpreter
gurleen singh<gs585@drexel.edu>
"""
import argparse
from parser import parse
import traceback

from evaluator import evaluate, load_file


def repl():
    """Provides a basic REPL."""
    print("gscheme")
    print("press ctrl+c to exit")
    while True:
        try:
            exp = input("> ")
            parsed = parse(exp)
            evaluated = evaluate(parsed)
            if evaluated is not None:
                print(evaluated)
        except KeyboardInterrupt:
            print("\nExiting...")
            quit()
        except Exception as e:
            traceback.print_exception(e)


def main():
    parser = argparse.ArgumentParser(description="a minimal scheme interpreter")
    parser.add_argument("filename", type=str, nargs="?", help="A scheme file to load")
    args = parser.parse_args()

    if args.filename is None:
        repl()
    else:
        load_file(args.filename)


if __name__ == "__main__":
    main()
