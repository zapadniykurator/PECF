__author__ = "Zedikon"
__copyright__ = "original evalsafe concept copyright by Zedikon 2022. Updated by zapadniy_kurator in 2026"

import ast
import math


MAX_EXPRESSION_LENGTH = 4096
MAX_AST_NODES = 200
MAX_POW_EXPONENT = 1024
MAX_RESULT_DIGITS = 100000


_SAFE_FUNCTIONS = {
    'abs': abs,
    'round': round,
    'min': min,
    'max': max,
    'pow': pow,
    'int': int,
    'float': float,
    'sqrt': math.sqrt,
    'sin': math.sin,
    'cos': math.cos,
    'tan': math.tan,
    'log': math.log,
    'log10': math.log10,
    'exp': math.exp,
    'floor': math.floor,
    'ceil': math.ceil,
}

_SAFE_CONSTANTS = {
    'pi': math.pi,
    'e': math.e,
    'tau': math.tau,
    'inf': math.inf,
}

_ALLOWED_NODE_TYPES = (
    ast.Expression,
    ast.Constant,
    ast.Name,
    ast.Load,
    ast.BinOp,
    ast.UnaryOp,
    ast.BoolOp,
    ast.Compare,
    ast.Call,
    ast.IfExp,
    ast.Tuple,
    ast.List,
    ast.Add,
    ast.Sub,
    ast.Mult,
    ast.Div,
    ast.FloorDiv,
    ast.Mod,
    ast.Pow,
    ast.UAdd,
    ast.USub,
    ast.Not,
    ast.And,
    ast.Or,
    ast.Eq,
    ast.NotEq,
    ast.Lt,
    ast.LtE,
    ast.Gt,
    ast.GtE,
)


class _UnsafeExpression(Exception):
    pass


def _validate_ast(tree):
    node_count = 0
    for node in ast.walk(tree):
        node_count += 1
        if node_count > MAX_AST_NODES:
            raise _UnsafeExpression("Expression is too complex")

        if not isinstance(node, _ALLOWED_NODE_TYPES):
            raise _UnsafeExpression(
                f"Node type {type(node).__name__} is not allowed"
            )

        if isinstance(node, ast.Name):
            if node.id.startswith("__") or node.id.endswith("__"):
                raise _UnsafeExpression(f"Name '{node.id}' is not allowed")

        if isinstance(node, ast.Call):
            if not isinstance(node.func, ast.Name):
                raise _UnsafeExpression("Only direct function calls are allowed")
            if node.keywords:
                raise _UnsafeExpression("Keyword arguments are not allowed")
            if any(isinstance(a, ast.Starred) for a in node.args):
                raise _UnsafeExpression("Starred arguments are not allowed")

        if isinstance(node, ast.Pow):
            exp = node.right
            if isinstance(exp, ast.Constant) and isinstance(exp.value, int):
                if abs(exp.value) > MAX_POW_EXPONENT:
                    raise _UnsafeExpression("Exponent is too large")


def _check_result(value):
    if isinstance(value, int) and not isinstance(value, bool):
        if value.bit_length() > MAX_RESULT_DIGITS * 3:
            raise _UnsafeExpression("Result is too large")
    elif isinstance(value, str):
        if len(value) > MAX_RESULT_DIGITS:
            raise _UnsafeExpression("Result is too large")
    return value


def evals(expression, variables=None):
    try:
        expression = str(expression)

        if len(expression) > MAX_EXPRESSION_LENGTH:
            return "Error: Expression is too long"

        if "__" in expression:
            return "Error: dunder access is not allowed"

        try:
            tree = ast.parse(expression, mode='eval')
        except SyntaxError as e:
            return f"Error: {e.msg}"

        try:
            _validate_ast(tree)
        except _UnsafeExpression as e:
            return f"Error: {e}"

        namespace = {}
        namespace.update(_SAFE_CONSTANTS)
        namespace.update(_SAFE_FUNCTIONS)

        if variables:
            for name, value in variables.items():
                if not isinstance(name, str):
                    continue
                if name.startswith("__") or name.endswith("__"):
                    continue
                if name in _SAFE_FUNCTIONS or name in _SAFE_CONSTANTS:
                    continue
                if callable(value):
                    continue
                if isinstance(value, type):
                    continue
                namespace[name] = value

        try:
            result = eval(
                compile(tree, '<pecf-eval>', 'eval'),
                {"__builtins__": {}},
                namespace,
            )
        except ZeroDivisionError:
            return "Error: Division by zero"
        except OverflowError:
            return "Error: Numeric overflow"
        except MemoryError:
            return "Error: Out of memory"
        except RecursionError:
            return "Error: Expression is too complex"

        try:
            return _check_result(result)
        except _UnsafeExpression as e:
            return f"Error: {e}"

    except Exception as e:
        return f"Error: {type(e).__name__}: {e}"