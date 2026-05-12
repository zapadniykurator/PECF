import parser

_global_variables = {}

def load_code(code):
    global _global_variables
    ast = parser.analyse(code)
    
    if isinstance(ast, str):
        return ast
    
    for item in ast:
        value = item[1][1][0]
        var_type = item[1][0]
        if var_type == "int" or var_type == "integer":
            try:
                value = int(value)
            except:
                pass
        elif var_type == "float":
            try:
                value = float(value)
            except:
                pass
        elif var_type == "eval":
            pass
        
        _global_variables[item[0]] = {
            "type": var_type,
            "value": value
        }
    
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