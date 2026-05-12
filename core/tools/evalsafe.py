__author__ = "Zedikon"
__copyright__ = "original evalsafe copyright by Zedikon 2022. Updated by zapadniy_kurator in 2026"

import math

def evals(expression, variables=None):
    try:
        expression = str(expression)
        allowed_names = {
            'abs': abs, 'round': round, 'min': min, 'max': max,
            'pow': pow, 'int': int, 'float': float,
            'pi': math.pi, 'e': math.e, 'sqrt': math.sqrt,
            'sin': math.sin, 'cos': math.cos, 'tan': math.tan
        }
        if variables:
            allowed_names.update(variables)
        code = compile(expression, '<string>', 'eval')
        for name in code.co_names:
            if name not in allowed_names and name != 'math':
                return f"Error: '{name}' is not allowed"
        
        result = eval(code, {"__builtins__": {}}, allowed_names)
        return result
    except ZeroDivisionError:
        return "Error: Division by zero"
    except Exception as e:
        return f"Error: {str(e)}"
