from .lexer import tokenize, LexerError, token_values


TYPE_TOKENS = {"string", "integer", "eval", "hex", "float"}


def _join_value(parts):
    out = ""
    prev = None
    for p in parts:
        if prev is None:
            out = p
        elif prev and p and prev[-1].isalnum() and p[0].isalnum():
            out += " " + p
        else:
            out += p
        prev = p
    return out


def analyse(code):
    try:
        stream = tokenize(code)
    except LexerError as e:
        return f"PECF lexer error: {e}"

    if not stream:
        return "PECF error: No valid definitions found"

    i = 0
    result = []
    n = len(stream)

    while i < n:
        ttype, tval, tpos = stream[i]

        if ttype == "next":
            i += 1
            continue

        if ttype != "word":
            return (
                f"PECF syntax error at {tpos}: "
                f"expected object name, got {tval!r}"
            )

        obj_name = tval
        i += 1

        if i >= n or stream[i][0] != "meaning":
            return f"PECF syntax error: expected ':' after '{obj_name}'"
        i += 1

        if i >= n:
            return f"PECF error: Missing value after {obj_name}:"

        next_type, next_val, _ = stream[i]

        if next_type in TYPE_TOKENS:
            token_type = next_type
            i += 1
        elif next_type == "word" and next_val in token_values:
            token_type = token_values[next_val]
            i += 1
        else:
            token_type = "string"

        if i < n and stream[i][0] == "meaning":
            i += 1

        value_parts = []
        while i < n and stream[i][0] != "next":
            value_parts.append(stream[i][1])
            i += 1

        value = _join_value(value_parts)

        result.append([obj_name, [token_type, [value]]])

        if i < n and stream[i][0] == "next":
            i += 1

    if not result:
        return "PECF error: No valid definitions found"

    return result