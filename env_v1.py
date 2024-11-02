# The EnvironmentManager class keeps a mapping between each variable (aka symbol)
# in a brewin program and the value of that variable - the value that's passed in can be
# anything you like. In our implementation we pass in a Value object which holds a type
# and a value (e.g., Int, 10).

class EnvironmentManager:
    def __init__(self):
        self.environment = {}
        self.local = {} # stack 
        
    def notInScope(self):
        self.local = {}

    # Gets the data associated a variable name
    def get(self, symbol):
        if symbol in self.local:
            return self.local[symbol]
        elif symbol in self.environment:
            return self.environment[symbol]
        return None

    # Sets the data associated with a variable name
    def set(self, symbol, value, isScope): # when to set the local and environment
        if (symbol not in self.environment) and (symbol not in self.local):
            return False
        if isScope and (symbol in self.local):
            self.local[symbol] = value
            return True
        self.environment[symbol] = value
        return True

    def create(self, symbol, start_val, isScope):
        if (symbol in self.environment) and (symbol not in self.local): 
            return False
        if isScope and (symbol not in self.local):
            self.local[symbol] = start_val 
            return True
        self.environment[symbol] = start_val 
        return True
        
            
