# gscheme

gscheme is a tiny Scheme interpreter written in Python 3.

It is far from complete. You can find all builtin functions in `env.py`.


## Usage

```bash
python3 main.py
```

```scheme
> (define fib (lambda (n) (if (< n 2) 1 (+ (fib (- n 1)) (fib (- n 2))))))
> (define range (lambda (a b) (if (= a b) (quote ()) (cons a (range (+ a 1) b)))))
> (map fib (range 0 10))
[1, 1, 2, 3, 5, 8, 13, 21, 34, 55]
```

Run from a file:
```bash
python3 main.py fib.scm
[1, 1, 2, 3, 5, 8, 13, 21, 34, 55]
```

## License
[MIT](https://choosealicense.com/licenses/mit/)