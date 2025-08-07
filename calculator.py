#!/usr/bin/env python3

import argparse
import ast
import math
import operator
import sys

try:
    import readline  # noqa: F401
except Exception:
    readline = None


class SafeEvaluator:
    """Safely evaluate arithmetic expressions with a restricted AST whitelist.

    Supported features:
    - Binary ops: +, -, *, /, //, %, **
    - Unary ops: +, -
    - Parentheses
    - Constants: integers, floats
    - Names: selected from math (e.g., pi, e)
    - Functions: selected math functions (e.g., sin, cos, tan, sqrt, log, exp, abs, round)
    """

    def __init__(self) -> None:
        self.binary_operators = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
            ast.FloorDiv: operator.floordiv,
            ast.Mod: operator.mod,
            ast.Pow: operator.pow,
        }
        self.unary_operators = {
            ast.UAdd: operator.pos,
            ast.USub: operator.neg,
        }
        # Whitelisted names and functions
        self.allowed_names = {
            name: getattr(math, name)
            for name in (
                # constants
                "pi",
                "e",
                "tau",
                "inf",
                "nan",
            )
        }
        # Basic builtins that are safe
        self.allowed_names.update({
            "abs": abs,
            "round": round,
            "min": min,
            "max": max,
        })
        # Common math functions
        for name in (
            "sin",
            "cos",
            "tan",
            "asin",
            "acos",
            "atan",
            "sqrt",
            "log",
            "log10",
            "exp",
            "pow",
            "degrees",
            "radians",
            "factorial",
            "hypot",
        ):
            self.allowed_names[name] = getattr(math, name)

    def evaluate(self, expression: str):
        try:
            parsed = ast.parse(expression, mode="eval")
        except SyntaxError as exc:
            raise ValueError(f"Syntax error: {exc.msg}") from exc
        return self._eval_node(parsed.body)

    def _eval_node(self, node):
        if isinstance(node, ast.BinOp):
            left = self._eval_node(node.left)
            right = self._eval_node(node.right)
            op_type = type(node.op)
            if op_type in self.binary_operators:
                return self.binary_operators[op_type](left, right)
            raise ValueError(f"Unsupported binary operator: {op_type.__name__}")

        if isinstance(node, ast.UnaryOp):
            operand = self._eval_node(node.operand)
            op_type = type(node.op)
            if op_type in self.unary_operators:
                return self.unary_operators[op_type](operand)
            raise ValueError(f"Unsupported unary operator: {op_type.__name__}")

        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return node.value
            raise ValueError("Only int and float constants are allowed")

        # For Python <3.8 compatibility where numbers might be ast.Num
        if hasattr(ast, "Num") and isinstance(node, getattr(ast, "Num")):
            return node.n

        if isinstance(node, ast.Name):
            if node.id in self.allowed_names:
                return self.allowed_names[node.id]
            raise ValueError(f"Name not allowed: {node.id}")

        if isinstance(node, ast.Call):
            func = self._eval_node(node.func)
            args = [self._eval_node(a) for a in node.args]
            if any(kw.arg is not None for kw in node.keywords):
                # Only allow positional args to keep surface small
                raise ValueError("Keyword arguments are not allowed")
            return func(*args)

        if isinstance(node, ast.Expr):
            return self._eval_node(node.value)

        if isinstance(node, ast.Tuple):
            return tuple(self._eval_node(e) for e in node.elts)

        raise ValueError(f"Unsupported expression: {type(node).__name__}")


_evaluator = SafeEvaluator()


def calculate(expression: str):
    """Calculate the result of an arithmetic expression safely."""
    return _evaluator.evaluate(expression)


def _format_result(value, precision: int = 12) -> str:
    if isinstance(value, bool):
        return str(int(value))
    if isinstance(value, int):
        return str(value)
    if isinstance(value, float):
        # Use general format with given precision to avoid overly long floats
        return format(value, f".{precision}g")
    # For tuples or other iterables, format each element
    if isinstance(value, (tuple, list)):
        return "[" + ", ".join(_format_result(v, precision) for v in value) + "]"
    return str(value)


def repl(precision: int = 12) -> int:
    print("Calculator REPL. Type expressions to evaluate. Type 'exit' or 'quit' to leave.")
    while True:
        try:
            line = input("calc> ")
        except EOFError:
            print()
            return 0
        except KeyboardInterrupt:
            print()
            return 130

        if not line:
            continue
        line = line.strip()
        if line.lower() in {"exit", "quit"}:
            return 0
        try:
            result = calculate(line)
            print(_format_result(result, precision))
        except Exception as exc:
            print(f"Error: {exc}")


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Safe CLI calculator")
    parser.add_argument(
        "expression",
        nargs=argparse.REMAINDER,
        help="Expression to evaluate. If omitted, starts an interactive REPL.",
    )
    parser.add_argument(
        "-p",
        "--precision",
        type=int,
        default=12,
        help="Floating point precision for output (default: 12)",
    )
    args = parser.parse_args(argv)

    if args.expression:
        expr = " ".join(args.expression)
        try:
            result = calculate(expr)
        except Exception as exc:
            print(f"Error: {exc}", file=sys.stderr)
            return 1
        print(_format_result(result, args.precision))
        return 0

    return repl(args.precision)


if __name__ == "__main__":
    raise SystemExit(main())