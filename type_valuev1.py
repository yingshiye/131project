from intbase import InterpreterBase


# Enumerated type for our different language data types
class Type:
    INT = "int"
    BOOL = "bool"
    STRING = "string"

# Represents a value, which has a type and its value
class Value:
    def __init__(self, type, value=None):
        self.t = type
        self.v = value

    def value(self):
        return self.v

    def type(self):
        return self.t


def create_value(val):
    if val == InterpreterBase.TRUE_DEF: # if the value is true
        return Value(Type.BOOL, True)
    elif val == InterpreterBase.FALSE_DEF: # the value is false
        return Value(Type.BOOL, False)
    elif isinstance(val, str): # if the value type is string 
        return Value(Type.STRING, val)
    elif isinstance(val, int): # if the value type if int
        return Value(Type.INT, val)
    else:
        raise ValueError("Unknown value type")


def get_printable(val): # change everything into string 
    if val.type() == Type.INT:
        return str(val.value())
    if val.type() == Type.STRING:
        return val.value()
    if val.type() == Type.BOOL:
        if val.value() is True:
            return "true"
        return "false"
    return None
