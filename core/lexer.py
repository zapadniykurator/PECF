tokens = {
    "meaning": ":",
    "string": "str",
    "integer": "int",
    "eval": "do",
    "hex": "hex",
    "float": "float",
    "comments": "//",
    "next": ";"
}

token_values = {v: k for k, v in tokens.items() if not isinstance(v, list)}
for op in tokens.get("operator", ""):
    token_values[op] = "operator"