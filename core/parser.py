from lexer import token_values

def analyse(code):
    words = []
    current_word = ""
    
    for char in code:
        if char == ';':
            if current_word:
                words.append(current_word)
                current_word = ""
            words.append(';')
        elif char == ' ':
            if current_word:
                words.append(current_word)
                current_word = ""
        else:
            current_word += char
    
    if current_word:
        words.append(current_word)
    
    i = 0
    result = []
    
    while i < len(words):
        current_word = words[i]
        if current_word.endswith(':'):
            obj_name = current_word[:-1]
            i += 1
            
            if i >= len(words):
                return f"PECF error: Missing value after {obj_name}:"
            
            token_word = words[i]
            token_type = None
            
            if token_word in token_values:
                token_type = token_values[token_word]
                i += 1
            elif token_word.endswith(':') and token_word[:-1] in token_values:
                token_type = token_values[token_word[:-1]]
                i += 1
            else:
                token_type = "string"
            
            value_parts = []
            while i < len(words) and words[i] != ';':
                value_parts.append(words[i])
                i += 1
            
            value = " ".join(value_parts)
            
            if i < len(words) and words[i] == ';':
                result.append([obj_name, [token_type, [value]]])
                i += 1
            else:
                return f"PECF syntax error! Missing ';' at the end of '{obj_name}' definition"
        
        else:
            return f"PECF syntax error! Expected object name ending with ':', got '{current_word}'"
    
    if not result:
        return "PECF error: No valid definitions found"
    
    return result
