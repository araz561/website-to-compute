# Calculator (Safe CLI)

A small, safe CLI calculator implemented in Python. It supports +, -, *, /, //, %, **, parentheses, and common math functions like sin, cos, sqrt, log, etc., plus constants like pi and e.

## Usage

- Evaluate a one-off expression:

```bash
python3 calculator.py "2 + 3 * (4 - 1)"
```

- Set output precision (significant digits for floats):

```bash
python3 calculator.py -p 8 "pi"
```

- Start interactive REPL:

```bash
python3 calculator.py
```
Then type expressions; use `exit` or `quit` to leave.

## Examples

```bash
$ python3 calculator.py "sqrt(9) + sin(pi/2)"
4

$ python3 calculator.py -p 6 "pi"
3.14159
```

## Run tests

```bash
python3 -m unittest -v
```
