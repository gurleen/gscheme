"""
provides a file i/o interface
to the gscheme language
"""

file_functions = {
    "open-input-file": lambda x: open(x, mode="r"),
    "open-output-file": lambda x: open(x, mode="w"),
    "close-input-port": lambda x: x.close(),
    "close-output-port": lambda x: x.close(),
    "read-line": lambda x: x.readline()
}