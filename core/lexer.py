tokens = {
    "meaning": ":",
    "string": "str",
    "integer": "int",
    "eval": "do",
    "hex": "hex",
    "float": "float",
    "comments": "//",
    "next": ";",
}

token_values = {v: k for k, v in tokens.items()}

_RAW_CHARS = set("+-*/%()[]{}<>=!&|^~.,")


class LexerError(Exception):
    pass


def tokenize(code):
    result = []
    i = 0
    n = len(code)
    sep = tokens["next"]
    meaning = tokens["meaning"]
    comment = tokens["comments"]

    while i < n:
        ch = code[i]

        if ch.isspace():
            i += 1
            continue

        if code.startswith(comment, i):
            while i < n and code[i] != "\n":
                i += 1
            continue

        if ch == meaning:
            result.append(("meaning", ch, i))
            i += 1
            continue

        if ch == sep:
            result.append(("next", ch, i))
            i += 1
            continue

        if ch.isdigit() or (ch == "." and i + 1 < n and code[i + 1].isdigit()):
            j = i
            seen_dot = False
            while j < n:
                c = code[j]
                if c.isdigit():
                    j += 1
                elif c == "." and not seen_dot:
                    seen_dot = True
                    j += 1
                else:
                    break
            result.append(("number", code[i:j], i))
            i = j
            continue

        if ch.isalpha() or ch == "_":
            j = i
            while j < n and (code[j].isalnum() or code[j] == "_"):
                j += 1
            word = code[i:j]
            if word in token_values:
                result.append((token_values[word], word, i))
            else:
                result.append(("word", word, i))
            i = j
            continue

        if ch in _RAW_CHARS:
            result.append(("raw", ch, i))
            i += 1
            continue

        raise LexerError(f"Unexpected character {ch!r} at position {i}")

    return result