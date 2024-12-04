from intbase import InterpreterBase
from type_valuev4 import Type, Value

class Closure: 

    def __init__(self, varName, varExpression, scope_snap):
        self.value = varExpression
        self.scope = scope_snap
        self.isEveluated = False

    def value(self):
        return self.value
    
    