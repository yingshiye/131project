# The EnvironmentManager class keeps a mapping between each variable (aka symbol)
# in a brewin program and the value of that variable - the value that's passed in can be
# anything you like. In our implementation we pass in a Value object which holds a type
# and a value (e.g., Int, 10).
from intbase import ErrorType
import copy 

class EnvironmentManager:
    
    def __init__(self):
        self.env_stack = []
        self.environment = [{}] # list of dict (try to act like stack?????)
        
    def notInScope(self):
        if len(self.environment) > 1:  
            self.environment.pop()
        
    def new_scope(self):
        self.environment.append({})
        
    def new_scope_func(self):  
        self.env_stack.append(self.environment)
        self.environment = [{}]
        # self.environment.append(func)
    
    def notInScope_func(self):
        self.environment = self.env_stack.pop()

    # Gets the data associated a variable name
    def get(self, symbol): # need to trace from the top to the bottom, in a stack or list
        reverse_list = list(reversed(self.environment))
        for dicti in reverse_list: #reverse a list, so sho
            if symbol in dicti:
                return dicti[symbol]
        return None
        # if symbol in self.environment[-1]: #reverse a list, so sho
        #     return self.environment[-1][symbol]
        # return None
        # if symbol in self.local:
        #     return self.local[symbol]
        # elif symbol in self.environment:
        #     return self.environment[symbol]
        # return None
    
    # Sets the data associated with a variable name
    def set(self, symbol, value): # when to set the local and environment
        # if (symbol not in self.environment) and (symbol not in self.local):
        #     return False
        # if isScope and (symbol in self.local):
        #     self.local[symbol] = value
        #     return True
        # self.environment[symbol] = value
        # return True
        # if self.isFuncEnv is False:
        reverse_list = reversed(self.environment)
        for dicti in reverse_list: #reverse a list, so sho
            if symbol in dicti:
                dicti[symbol] = value
                return True
        return False
        # else: 
            # reverse_list = reversed(self.func)
            # for dicti in reverse_list: #reverse a list, so sho
            #     if symbol in dicti:
            #         dicti[symbol] = value
            #         return True
            # return False

    def create(self, symbol, start_val):
        # if (symbol in self.environment) and (symbol in self.local): 
        #     return False
        # if isScope and (symbol not in self.local):
        #     self.local[symbol] = start_val 
        #     return True
        # self.environment[symbol] = start_val 
        # return True
        # if self.isFuncEnv is False:
        if symbol in self.environment[-1]:
            return False
        else:
            self.environment[-1][symbol] = start_val
            return True
        # else:
        #     if symbol in self.func[-1]:
        #         return False
        #     else:
        #         self.func[-1][symbol] = start_val
        #         return True