from . import parser
from .tools import evals


_global_variables = {}


def _coerce(name, var_type, value):
    if var_type in ("int", "integer"):
        try:
            return int(value)
        except (ValueError, TypeError):
            pass
    elif var_type == "float":
        try:
            return float(value)
        except (ValueError, TypeError):
            pass
    elif var_type == "hex":
        try:
            return int(value, 16)
        except (ValueError, TypeError):
            pass
    elif var_type == "eval":
        ctx = {k: v["value"] for k, v in _global_variables.items()}
        result = evals(value, ctx)
        if isinstance(result, str) and result.startswith("Error"):
            return result
        return result

    if var_type in ("int", "integer", "float"):
        ctx = {k: v["value"] for k, v in _global_variables.items()}
        result = evals(value, ctx)
        if isinstance(result, str) and result.startswith("Error"):
            return f"PECF error in '{name}': {result}"
        if var_type in ("int", "integer") and isinstance(result, float) and result.is_integer():
            return int(result)
        return result

    return value


def load_code(code):
    global _global_variables
    ast = parser.analyse(code)

    if isinstance(ast, str):
        return ast

    deferred = []
    for item in ast:
        name, (var_type, (value,)) = item
        if var_type == "eval":
            deferred.append((name, var_type, value))
            continue
        coerced = _coerce(name, var_type, value)
        if isinstance(coerced, str) and coerced.startswith("PECF error"):
            return coerced
        _global_variables[name] = {"type": var_type, "value": coerced}

    for name, var_type, value in deferred:
        coerced = _coerce(name, var_type, value)
        if isinstance(coerced, str) and coerced.startswith("PECF error"):
            return coerced
        _global_variables[name] = {"type": var_type, "value": coerced}

    return [[name, [data["type"], [data["value"]]]] for name, data in _global_variables.items()]


def return_variable(var_name):
    global _global_variables
    if not _global_variables:
        return "No code loaded"
    if var_name in _global_variables:
        return _global_variables[var_name]["value"]
    return f"Variable '{var_name}' not found"


def get_variable_type(var_name):
    global _global_variables
    if not _global_variables:
        return "No code loaded"
    if var_name in _global_variables:
        return _global_variables[var_name]["type"]
    return f"Variable '{var_name}' not found"


def get_all_variables():
    global _global_variables
    return {name: data["value"] for name, data in _global_variables.items()}


def get_ast():
    global _global_variables
    return [[name, [data["type"], [data["value"]]]] for name, data in _global_variables.items()]


def clear():
    global _global_variables
    _global_variables = {}