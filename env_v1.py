# The EnvironmentManager class keeps a mapping between each variable (aka symbol)
# in a brewin program and the value of that variable - the value that's passed in can be
# anything you like. In our implementation we pass in a Value object which holds a type
# and a value (e.g., Int, 10).

class EnvironmentManager:
    def __init__(self):
        self.environment = [{}] # list of dict (try to act like stack?????)
        
    def notInScope(self):
        self.environment.pop()
        
    def new_scope(self):
        if len(self.environment) > 1:
            self.environment.append({})

    # Gets the data associated a variable name
    def get(self, symbol): # need to trace from the top to the bottom, in a stack or list
        reverse_list = list(reversed(self.environment))
        for dicti in reverse_list: #reverse a list, so sho
            if symbol in dicti:
                return dicti[symbol]
        return None
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
        reverse_list = list(reversed(self.environment))
        for dicti in reverse_list: #reverse a list, so sho
            if symbol in dicti:
                dicti[symbol] = value
                return True
        return False

    def create(self, symbol, start_val):
        # if (symbol in self.environment) and (symbol in self.local): 
        #     return False
        # if isScope and (symbol not in self.local):
        #     self.local[symbol] = start_val 
        #     return True
        # self.environment[symbol] = start_val 
        # return True
        if symbol not in self.environment[-1]:
            self.environment[-1][symbol] = start_val
            return True
        return False
        
        
