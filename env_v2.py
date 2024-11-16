from intbase import InterpreterBase

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
            return result
                
        return None

    def set(self, symbol, value):
        cur_func_env = self.environment[-1]
        if "." not in symbol:
            for env in reversed(cur_func_env):
                if symbol in env:
                    if (self.checkType(env[symbol], value)):
                        env[symbol] = value
                        return True
                    return "type error"
        
        elif "." in symbol: 
            symbol_value = self.find_var_in_struct(symbol)
            if (self.checkType(symbol_value, value)):
                symbol_value.v = value.value()
                return True
            # print(type(value_O))
            # print((type(value)))

        return False
    
    def checkType(self, obj1, obj2):
        if obj1.type() == obj2.type():
            return True
        elif obj1.type() == "bool" and obj2.type() == "int": 
            obj2.t = "bool"
            if obj2.value() == 0: 
                obj2.v = False
            else:
                obj2.v = True
            return True
        else: 
            return False

    # create a new symbol in the top-most environment, regardless of whether that symbol exists
    # in a lower environment
    def create(self, symbol, value):
        cur_func_env = self.environment[-1]
        if symbol in cur_func_env[-1]:   # symbol already defined in current scope
            return False
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
        field_list = reversed(self.environment[-1])
        while "." in symbol: 
            var_name, symbol = symbol.split('.', 1)
            # print(symbol)
            for env in field_list:
                if var_name in env:
                    field_list = env
        # return field_list
        
        if field_list is not None:
            for i in field_list:
                if symbol == i:
                    return field_list[i] 