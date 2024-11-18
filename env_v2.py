from intbase import InterpreterBase
from type_valuev2 import Type, Value
# The EnvironmentManager class keeps a mapping between each variable name (aka symbol)
# in a brewin program and the Value object, which stores a type, and a value.
class EnvironmentManager:
    def __init__(self):
        self.environment = []

    # returns a VariableDef object
    def get(self, symbol):
        cur_func_env = self.environment[-1]
        if "." not in symbol:
            for env in reversed(cur_func_env):
                if symbol in env:
                    return env[symbol]  

        elif "." in symbol: 
            result = self.find_var_in_struct(symbol)
            if result == "type error":
                return "type error"
            if result == "fault error":
                return "fault error"
            if result == "name error": 
                return "name error"
            return result
                
        return None

    def set(self, symbol, value):
        cur_func_env = self.environment[-1]
        if "." not in symbol:
            for env in reversed(cur_func_env):
                if symbol in env:
                    if (self.checkType(env[symbol], value)):
                        if env[symbol].type() == "bool" and value.type() == "int":
                            if value.value() != 0:
                                env[symbol] = Value(Type.BOOL, True)
                            else: 
                                env[symbol] = Value(Type.BOOL, False)
                        else: 
                            env[symbol] = value
                        return True
                    return "type error"
        
        elif "." in symbol: 
            symbol_value = self.find_var_in_struct(symbol)
            if symbol_value == "type error":
                return "type error"
            if symbol_value == "fault error":
                return "fault error"
            if symbol_value == "name error": 
                return "name error"
            if (self.checkType(symbol_value, value)):
                if symbol_value.type() == "bool" and value.type() == "int":
                    if value.value() != 0:
                        value = Value(Type.BOOL, True)
                        symbol_value.v = value.value()
                    else: 
                        value = Value(Type.BOOL, False)
                        symbol_value.v = value.value()
                else: 
                    symbol_value.v = value.value()
                return True
            else: 
                return "type error"
            # print(type(value_O))
            # print((type(value)))

        return False
    
    def checkType(self, obj1, obj2):
        if obj1.type() == obj2.type():
            return True
        elif obj1.type() == "bool" and obj2.type() == "int": 
            return True
        elif (obj1.type() in Type.struct_list and obj2.type() == "nil") or (
            obj1.type() == "nil" and obj2.type() in Type.struct_list
        ):
            return True
        else: 
            return False

    # create a new symbol in the top-most environment, regardless of whether that symbol exists
    # in a lower environment
    def create(self, symbol, value):
        cur_func_env = self.environment[-1]
        if symbol in cur_func_env[-1]:   # symbol already defined in current scope
            return False
        if not Type.valid_type(value.type()): 
            return "type error"
        cur_func_env[-1][symbol] = value
        return True

    # used when we enter a new function - start with empty dictionary to hold parameters.
    def push_func(self):
        self.environment.append([{}])  # [[...]] -> [[...], [{}]]

    def push_block(self):
        cur_func_env = self.environment[-1]
        cur_func_env.append({})  # [[...],[{....}] -> [[...],[{...}, {}]]

    def pop_block(self):
        cur_func_env = self.environment[-1]
        cur_func_env.pop() 

    # used when we exit a nested block to discard the environment for that block
    def pop_func(self):
        self.environment.pop()

    def find_var_in_struct(self, symbol):
        fields = symbol.split('.')
        var = None
        # print(field)

        for env in reversed(self.environment[-1]):
            if fields[0] in env:
                var = env[fields[0]] #find the variable in the environment
        
        if var is None: 
            return "name error"
        if var.type() == "nil" or var.value() == "nil": 
            return "fault error"
        if var.type() not in Type.struct_list:
            return "type error"
        
        for field in fields[1:]:
            if var.type() == "nil" or var.value() == "nil" or var.value() == None: 
                return "fault error"
            if field != fields[-1] and var.type() not in Type.struct_list:
                return "type error"
            # if field == fields[-1] and field.type() not in ["string", "bool", "int"]:
            #     return "type error"
            if field in var.value():
                var = var.value()[field]
            else: 
                return "name error"

        return var 

        # field_list = reversed(self.environment[-1])
        # while "." in symbol: 
        #     var_name, symbol = symbol.split('.', 1)
        #     # print(symbol)
        #     for env in field_list:
        #         if var_name in env:
        #             field_list = env
        # # return field_list
        
        # if field_list is not None:
        #     for i in field_list:
        #         if symbol == i:
        #             return field_list[i] 